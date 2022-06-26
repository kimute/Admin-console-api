import os
from fastapi import APIRouter, Depends
#from common.conn import get_db, get_ro_db, get_sp_db, get_sp_ro_db
from common.conn import get_sp_db, get_sp_ro_db
from sqlalchemy.orm import Session
from jwks.auth_jwks import get_current_user, get_jwt
from models.model import UserRegister, EditUser
from starlette.responses import JSONResponse
from controller.api_call import api_req
from controller.crud_user import user_edit, user_delete, user_register


router = APIRouter()


@router.post("/create_user/{role}")
async def register(
        reg_info: UserRegister,
        role: int,
        db_sp: Session = Depends(get_sp_db),
        db_sp_ro: Session = Depends(get_sp_ro_db),
        jwt: str = Depends(get_jwt),
        claims: str = Depends(get_current_user)):
    '''
     User create API\n
    :param SP role:\n
      - Admin(1), CU(2), User(3)\n
    :param UserRegister:\n
      - email, password, name(for SP console)
    '''
    result = await user_register(role, reg_info, db_sp, db_sp_ro, jwt, claims)
    if result:
        return JSONResponse(status_code=200, content=dict(
                                result="user create success"))
    return JSONResponse(status_code=400, content=dict(
                                result="user create failed"))


@router.put("/edit_user")
async def edit_user(edit_user: EditUser,
              db_sp: Session = Depends(get_sp_db),
              db_sp_ro: Session = Depends(get_sp_ro_db),
              jwt: str = Depends(get_jwt),
              claims: str = Depends(get_current_user)):
    '''
     User edit API\n
    :param SP role:\n
      - Admin(1), CU(2), User(3)\n
    :param userID:\n
      - id: target user id
      - pw: new password
    '''
    result = await user_edit(edit_user, db_sp, db_sp_ro, jwt, claims)
    if result:
        return JSONResponse(status_code=200, content=dict(
                                result="edit success"))
    return JSONResponse(status_code=400, content=dict(
                                result="edit failed"))


@router.delete("/delete_user/{userId}")
async def delete_user(userId: str,
                db_sp: Session = Depends(get_sp_db),
                db_sp_ro: Session = Depends(get_sp_ro_db),
                jwt: str = Depends(get_jwt),
                claims: str = Depends(get_current_user)):
    '''
    User delete API\n
    :param userID:\n
      - userId: target user id
    '''

    result = await user_delete(userId, db_sp, db_sp_ro, jwt, claims)
    if result:
        return JSONResponse(status_code=200, content=dict(
                                result="delete success"))
    return JSONResponse(status_code=400, content=dict(
                                result="delete failed"))
