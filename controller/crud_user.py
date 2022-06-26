import os
import logging
from dotenv import load_dotenv
from datetime import datetime
from models.model import UsersTable
from models.model_ro import UsersTable_ro
#from models.cognito import Cognito
#from models.cognito_ro import Cognito_ro
from controller.aws_cognito import cognito_auth, cognito_reset_pass, cognito_delete
from starlette.responses import JSONResponse
from controller.api_call import api_req

load_dotenv()

cm_api = os.getenv('CM_INTERNAL_API_BASE_URL')
companyCode = os.getenv('COMPANY_CODE')


logging.basicConfig(encoding='utf-8', level=logging.DEBUG)


async def user_register(role, reg_info, db_sp, db_sp_ro, jwt, claims):
    role = role
    email = reg_info.email
    password = reg_info.pw
    name = reg_info.name
    adminUserRole=32

    if claims:
        current_user = db_sp_ro.query(UsersTable_ro).\
                    filter(
                        UsersTable_ro.userId == claims['email']
                        ).first()
        logging.debug(current_user.role)
        if current_user.role == 1:
            data = {}
            data["user"] = {}
            data["user"]["companyCode"] = companyCode
            data["user"]["password"] = password
            data["user"]["roleCode"] = str(adminUserRole)
            data["user"]["email"] = email
            path = cm_api+'adminUserRegister'
            logging.debug(path)
            logging.debug(data)
            try:
                response = await api_req(path, 'POST', jwt, data)
                logging.debug("sp console | cm API post:")
                logging.debug(response.text)
                logging.debug(response.content)
            except Exception as e:
                logging.error(
                    'SP console API | CM API get failed:{}'.format(e))
                return False

            if response.status_code == 200:
                response = response.json()
                cognito_id = response["id"]
                try:
                    newUser = UsersTable()
                    newUser.userId = email
                    newUser.name = name
                    newUser.role = role
                    newUser.cognitoId = cognito_id
                    newUser.created_at = datetime.utcnow()
                    db_sp.add(newUser)
                    db_sp.commit()
                    return True
                except Exception as e:
                    logging.error(
                            'SP console API | register failed:{}'.format(e))
                    db_sp.rollback()
                    return False
            return False

        logging.error('SP console API | not authorized user')
        return False


async def user_edit(edit_user, db_sp, db_sp_ro, jwt, claims):
    if claims:
        # 修正するUSER
        current_user = db_sp_ro.query(UsersTable_ro).\
            filter(UsersTable_ro.userId == claims['email']).first()
        if current_user.role == 1:
            try:
                # 修正対象USER
                editUser = db_sp.query(UsersTable).\
                    filter(UsersTable.id == edit_user.id).first()
                if not editUser:
                    return JSONResponse(status_code=400,
                                        content=dict(
                                            result="user:{} is not found"
                                            .format(edit_user.email)))
                else:
                    data = {}
                    data["user"] = {}
                    data["user"]['password'] = edit_user.pw
                    edit_id = editUser.cognitoId
                    path = cm_api+'adminUser/'+companyCode+'/'+str(edit_id)
                    user_cognito = await api_req(path, 'PUT', jwt, data)
                    logging.info("sp console | cm API put:")
                    logging.info(user_cognito)
                    if user_cognito.status_code == 200:
                        editUser.updated_at = datetime.utcnow()
                        editUser.role = edit_user.role
                        db_sp.merge(editUser)
                        db_sp.commit()
                        return True
                    return user_cognito.json()

            except Exception as e:
                logging.error('SP console API | edit_user:{}'.format(e))
                db_sp.rollback()
                return False

        logging.error('SP console API | not authorized user')
        return False


async def user_delete(userId, db_sp, db_sp_ro, jwt, claims):
    if claims:
        current_user = db_sp_ro.query(UsersTable_ro).\
            filter(UsersTable_ro.userId == claims['email']).first()
        if current_user.role == 1:
            try:
                targetUser = db_sp.query(UsersTable).\
                    filter(UsersTable.id == userId).first()
                if not targetUser:
                    logging.error(
                        'SP console API | user:{}is not found'.format(userId))
                    return False
                else:
                    target = targetUser.cognitoId
                    path = cm_api+'adminUser/'+companyCode+'/'+str(target)
                    delete_cognito = await api_req(path, 'DELETE', jwt)
                    if delete_cognito.status_code == 200:
                        db_sp.delete(targetUser)
                        db_sp.commit()
                        return True
                    return delete_cognito.json()

            except Exception as e:
                logging.error('SP console API | delete_user:{}'.format(e))
                db_sp.rollback()
                return False

        logging.error('SP console API | not authorized user')
        return False
