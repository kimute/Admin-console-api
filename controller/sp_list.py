import os
import re
import json
import os.path
import logging
from dotenv import load_dotenv
from datetime import datetime
from models.spInfo import SpInfoTable
from models.spInfo_ro import SpInfoTable_ro
from models.company import CompanyTable
from models.sequence_manager import SequenceTable
from models.sequence_manager_ro import SequenceTable_ro
from controller.api_call import api_req
from common.consts import external_system, staff_code, operationid, prefectures_code, category, sub_domain
from controller.aws_cognito import upload_json, delete_json


load_dotenv()

cm_api = os.getenv('CM_INTERNAL_API_BASE_URL')

logging.basicConfig(encoding='utf-8', level=logging.DEBUG)


async def sp_list_all(db_sp, db_sp_ro, jwt, claims):
    if claims:
        try:
            sp_list = db_sp_ro.query(SpInfoTable_ro).all()
            company_list = []
            for i in range(len(sp_list)):
                companys = dict(
                    company_code=sp_list[i].companyCode,
                    company_name=sp_list[i].companyName,
                    oem=sp_list[i].oem,
                    url=sp_list[i].spUrl,
                    status=sp_list[i].status
                )
                company_list.append(companys)
            path = cm_api + 'addSpManagementList'
            data = {
                "SpManagement": []
            }
            for i in company_list:
                data["SpManagement"].append(i['company_code'])

            logging.debug("cM API post data:{}".format(data))

            response = await api_req(path, 'POST', jwt, data)

            logging.debug("cM API response:{}".format(response))

            if response.status_code == 200:
                resp_data = response.json()
                # SP response data check
                logging.debug("cM API resp_data:{}".format(resp_data))
                logging.debug("cM API company_list:{}".format(company_list))
                # SP DB update
                for cm_data in resp_data['addSpManager']:
                    resp_company = cm_data
                    logging.debug("cM API cm_data:{}".format(resp_company))
                    for j in range(len(company_list)):
                        list_company = company_list[j]
                        logging.debug("cM API compnay_list loop:{}".format(list_company))
                        logging.debug("SP consol API | company code check")
                        if resp_company["companyCode"] == list_company ["company_code"]:
                            # status check
                            if resp_company["status"] != list_company["status"]:
                                logging.debug("SP consol API | status update")
                                check_company =resp_company['companyCode']
                                logging.debug("SP consol API | check_company:{}".format(check_company))
                                get_sp = db_sp.query(SpInfoTable).\
                                    filter(
                                        SpInfoTable.companyCode == check_company).first()
                                if get_sp is not None:
                                    logging.debug("SP consol API | resp_company['status']:{}".format(resp_company['status']))
                                    get_sp.status = resp_company['status']
                                    db_sp.merge(get_sp)
                                    db_sp.commit()
                                logging.error(
                                    "SP consol API | status update error")
                                db_sp.rollback()
                            else:
                                break

            return company_list
        except Exception as e:
            logging.error(
                    'SP console API | sp_list_all():{}'.format(e))
            return False


def sp_list_search(company_name, db_sp_ro, claims):
    if claims:
        try:
            company = db_sp_ro.query(SpInfoTable_ro).\
                filter(SpInfoTable_ro.companyName == company_name).first()
            company_list = []
            get_company = dict(
                    company_code=company.companyCode,
                    company_name=company.companyName,
                    oem=company.oem,
                    url=company.spUrl
                )
            company_list.append(get_company)
            return company_list
        except Exception as e:
            logging.error(
                    'SP console API | sp_list_search():{}'.format(e))

            return False


async def get_sp_details(company_name, jwt, claims):
    if claims:
        try:
            path = cm_api+company_name
            logging.debug(path)
            response = await api_req(path, 'GET', jwt)
            logging.debug(response)
            return response.json()
        except Exception as e:
            logging.error(
                    'SP console API | get_sp_details():{}'.format(e))
            return False


def target_sp_delete(company_name, db_sp, claims):
    try:
        target_company = db_sp.query(SpInfoTable).\
            filter(SpInfoTable.companyName == company_name).first()
        if not target_company:
            logging.error(
            'SP console API | company:{}is not found'.format(target_company))
            return False
        else:
            # cM API処理 if ok then below run
            db_sp.delete(target_company)
            db_sp.commit()
            return True

    except Exception as e:
        logging.error('SP console API | sp_delete error:{}'.format(e))
        return False


async def sp_register(sp_info, db_sp, db_sp_ro, jwt, claims):
    company_name = sp_info.companyInfo.companyName
    domain_sub_check = sp_info.companyInfo.subDomain
    domain_name_check = sp_info.companyInfo.domain
    company_category = sp_info.companyInfo.companyCategory
    domain_name = domain_name_check+domain_sub_check
    honbu_check = sp_info.companyInfo.honbuCode
    ssl_arn = ""
    zone_id = ""
    store_code = {}
    stores = []
    for i in range(len(sp_info.storeInfos)):
        store_num = str(10000000 + i+1)
        list_num = list(store_num)
        list_num[0] = '0'
        store_num = "".join(list_num)
        store_code[sp_info.storeInfos[i].externalSystemStoreName] = store_num
        store_prefectures_code = prefectures_code[sp_info.storeInfos[i].prefectures]
        store = dict(
            store_code=store_num,
            area_code="",
            store_name=sp_info.storeInfos[i].storeName,
            external_system_store_name=sp_info.storeInfos[i].externalSystemStoreName,
            zip_code=sp_info.storeInfos[i].zipCode,
            prefectures_name=sp_info.storeInfos[i].prefectures,
            prefectures_code=store_prefectures_code,
            address1=sp_info.storeInfos[i].municipalities,
            address2=sp_info.storeInfos[i].address,
            address3=sp_info.storeInfos[i].building,
            phone_number=sp_info.storeInfos[i].phoneNumber
        )
        stores.append(store)
        logging.debug('store:{}'.format(store))

    # userId check
    staffs = []
    checked_email = ""
    checked_user_name = ""
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    for i in range(len(sp_info.staffInfos)):
        staff_num = str(10000000 + i+1)
        list_staff = list(staff_num)
        list_staff[0] = '0'
        staff_num = "".join(list_staff)
        role_name = str(sp_info.staffInfos[i].staffRoleName)
        role = staff_code[role_name]
        id_check = sp_info.staffInfos[i].userId
        cognito_pass = sp_info.staffInfos[i].password
        if(re.fullmatch(regex, id_check)):
            logging.debug('Email format:{}'.format(id_check))
            user_pool = os.environ['STAFF_USERPOOL_ID']
            checked_email = id_check
            checked_user_name = ""
        else:
            logging.debug('User name format:{}'.format(id_check))
            user_pool = os.environ['USERNAME_USERPOOL_ID']
            checked_email = ""
            checked_user_name = id_check

        code_length = len(sp_info.staffInfos[i].externalSystemStoreName)

        store_name = sp_info.staffInfos[i].externalSystemStoreName

        logging.debug('add store_code:{}'.format(store_code))

        find_code = []
        for j in range(code_length):
            find_code.append(store_code[store_name[j]])

        logging.debug('find_code:{}'.format(find_code))

        staff = dict(
            email=checked_email,
            user_name=checked_user_name,
            role_name=str(role),
            user_code=staff_num,
            last_name=sp_info.staffInfos[i].lastNameKanji,
            first_name=sp_info.staffInfos[i].firstNameKanji,
            last_name_kana=sp_info.staffInfos[i].lastNameFurigana,
            first_name_kana=sp_info.staffInfos[i].firstNameFurigana,
            store_code=find_code,
            cognito_password=cognito_pass,
            username_userpool_id=user_pool,
        )
        staffs.append(staff)
        logging.debug('staff:{}'.format(staff))

    if claims:
        logging.debug('company_category:{}'.format(company_category))
        try:
            company = db_sp_ro.query(SpInfoTable_ro).\
                filter(SpInfoTable_ro.companyName == company_name).first()
            if company is not None:
                logging.error(
                    'SP console API | sp already exist:{}'.format(company))
                return False

            if company is None:
                seq_manager = db_sp.query(SequenceTable).\
                    filter(SequenceTable.type == company_category).first()
                get_last_num = int(seq_manager.value)
                try:
                    seq_manager.value = get_last_num+1
                    db_sp.merge(seq_manager)
                    db_sp.commit()
                except Exception as e:
                    logging.error(
                        'SP console API | sequence update failed:{}'.format(e))
                    db_sp.rollback()
                if company_category == "正規":
                    before = category[company_category] + get_last_num+1
                    list_num = list(str(before))
                    list_num[0] = '0'
                    new_sp_num = "".join(list_num)
                else:
                    new_sp_num = category[company_category] + get_last_num+1

                trans_num = str(new_sp_num)
                logging.debug('new sp number:{}'.format(trans_num))
                system = sp_info.companyInfo.externalSystem
                # lotas check
                check_lotas = sub_domain[domain_sub_check]
                l_list = ["LOTAS", "STGLOTAS", "DEVLOTAS"]
                is_lotas_check = "Lotas" if check_lotas in l_list else ""
                # ssl_arn check
                if check_lotas in l_list:
                    ssl_arn = os.environ['LOTAS_SSL_ARN']
                    zone_id = os.environ['LOTAS_ZONE_ID']
                else:
                    ssl_arn = os.environ['DOMAIN_SSL_ARN']
                    zone_id = os.environ['ZONE_ID']

                logging.debug('is_lotas_check:{}'.format(is_lotas_check))

                # honbu check
                def hasNumber(stringVal):
                    return any(elem.isdigit() for elem in stringVal)
                is_honbu_check = honbu_check if hasNumber(honbu_check) else ""
                logging.debug('is_honbu_check:{}'.format(is_honbu_check))

                # owner code check
                owners = list(
                    filter(lambda x: x['role_name'] == '21', staffs))
                owner_code = owners[0]['user_code']

                company_json = {
                                "external_system_type":
                                external_system[system],
                                "external_system_type_2": "",
                                "schema_name": os.environ['SCHEMA_NAME'],
                                "api_userpool_id":
                                os.environ['API_USERPOOL_ID'],
                                "staff_userpool_id":
                                os.environ['STAFF_USERPOOL_ID'],
                                "username_userpool_id":
                                os.environ['USERNAME_USERPOOL_ID'],
                                "carsSERVICE_password":
                                os.environ['CARSSERVICE_PASSWORD'],
                                "DIC_api_password":
                                os.environ['DIC_API_PASSWORD'],
                                "survey_password":
                                os.environ['SURVEY_PASSWORD'],
                                "operationid": operationid,
                                "domain_name": domain_name,
                                "domain": domain_sub_check,
                                "domain_ssl_arn": ssl_arn,
                                "zone_id": zone_id,
                                "company_code": trans_num,
                                "owner_staff_code": owner_code,
                                "company_name": company_name,
                                "company_representative":
                                sp_info.companyInfo.ownerName,
                                "zip_code": sp_info.companyInfo.zipCode,
                                "company_prefectures_name":
                                sp_info.companyInfo.prefectures,
                                "company_prefectures_code":
                                prefectures_code[
                                    sp_info.companyInfo.prefectures],
                                "address1": sp_info.companyInfo.municipalities,
                                "address2": sp_info.companyInfo.address,
                                "address3": sp_info.companyInfo.building,
                                "phone_number":
                                sp_info.companyInfo.phoneNumber,
                                "company_email": sp_info.companyInfo.email,
                                "company_employee_count":
                                sp_info.companyInfo.employeeCount,
                                "company_shop_count":
                                sp_info.companyInfo.storeCount,
                                "first_month_of_the_year":
                                sp_info.companyInfo.firstMonthOfTheYear,
                                "contract_max_store":
                                sp_info.companyInfo.maxStore,
                                "contract_max_staff":
                                sp_info.companyInfo.maxStaff,
                                "contract_start_date":
                                sp_info.companyInfo.contractStartDate,
                                "contract_end_date":
                                sp_info.companyInfo.contractEndDate,
                                "honbu_code": is_honbu_check,
                                "is_lotas": is_lotas_check,
                                "stores": stores,
                                "external_system_stores": [],
                                "staffs": staffs
                               }

                logging.debug('company_json:{}'.format(company_json))

                json_data = json.dumps(company_json, ensure_ascii=False)

                if json_data:
                    bucket = os.environ['BUCKET_NAME']
                    folder_name = 'AddSP'
                    file_name = trans_num+'.json'
                    key = folder_name+'/'+file_name
                    result = upload_json(bucket, key, json_data)
                    if result:
                        try:
                            req_data = {}
                            data = {}
                            data['fileName'] = file_name
                            data['status'] = 0
                            req_data['SpManagement'] = data
                            logging.debug('cM_post_data:{}'.format(req_data))
                            path = cm_api + 'addSpManagement/'+str(trans_num)
                            logging.debug('cM API path:{}'.format(path))
                            # connection to cM API[POST]
                            response = await api_req(path, 'POST', jwt, req_data)
                            if response.status_code == 200:
                                newSp = SpInfoTable()
                                newSp.companyCode = trans_num
                                newSp.companyName = company_name
                                newSp.oem = sp_info.companyInfo.oemType
                                newSp.spUrl = domain_name
                                newSp.insertAt = datetime.utcnow()
                                newSp.status = 0
                                db_sp.add(newSp)
                                db_sp.commit()
                                return_value = {
                                    "company_code": trans_num,
                                    "env": sub_domain[domain_sub_check],
                                }
                                return return_value
                            return False
                        except Exception as e:
                            logging.error(
                                'SP API | cM API/DB error:{}'.format(e))
                            db_sp.rollback()
                            delete_json(bucket, key)
                            return False

                    else:
                        logging.error(
                            'SP console API | s3 failed:{}'.format(result))
                        db_sp.rollback()
                        return False
                else:
                    logging.error(
                        'SP console API | json error:{}'.format(json_data))
                    return False

        except Exception as e:
            logging.error(
                    'SP console API | sp_register failed:{}'.format(e))
            db_sp.rollback()
            return False
