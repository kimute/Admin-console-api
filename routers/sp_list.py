import os
import re
import json
import logging
from dotenv import load_dotenv
from datetime import datetime
from models.spInfo import SpInfoTable
from models.spInfo_ro import SpInfoTable_ro
from models.company import CompanyTable
from models.sequence_manager import SequenceTable
from models.sequence_manager_ro import SequenceTable_ro
from common.consts import external_system, staff_code, operationid, prefectures_code, category, sub_domain
from controller.aws_cognito import upload_json, delete_json
from controller.api_call import api_req

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
            #response = await api_req(path, 'POST', jwt, data)
            response = {"status_code": 200} # <-tedt用
            if response['status_code'] == 200: #response.status_code == 200:
                #resp_data = response.json()
                resp_data = [
                    {
                      "companyCode": "90000069",
                      "fileName": "90000069.json",
                      "status": 1
                    },
                    {
                      "companyCode": "90000070",
                      "fileName": "90000070.json",
                      "status": 1
                    }
                ]
                # SP DB update
                for cm_data in resp_data:
                    for sp_data in company_list:
                        # company code check
                        if cm_data['companyCode'] == sp_data['company_code']:
                            # status check
                            if cm_data['status'] != sp_data['status']:
                                logging.debug("SP consol API | status update")
                                get_sp = db_sp.query(SpInfoTable).\
                                    filter(
                                        SpInfoTable.companyCode == cm_data['companyCode']).first()
                                if get_sp is not None:
                                    get_sp.status = cm_data['status']
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


async def sp_list_search(company_name, db_sp_ro, claims):
    if claims:
        try:
            company = db_sp_ro.query(SpInfoTable_ro).\
                filter(SpInfoTable_ro.companyName == company_name).first()
            company_list = []
            get_company = dict(
                    company_code=company.companyCode,
                    company_name=company.companyName,
                    oem=company.oem,
                    url=company.spUrl,
                    insert_at=company.insertAt,
                    update_at=company.updateAt,
                    delete_at=company.deleteAt,
                    delete_flag=company.deleteFlag,
                    status=company.status
                )
            company_list.append(get_company)
            return company_list
        except Exception as e:
            logging.error(
                    'SP console API | sp_list_search():{}'.format(e))

            return False


def get_sp_details(company_code, db, jwt, claims):
    if claims:
        try:
            '''
            company = db.query(CompanyTable).\
                filter(CompanyTable.companyCode == company_code).first()
            company_details = []
            get_details = dict(
                companyCode=company.companyCode,
                ownerStaffCode=company.ownerStaffCode,
                companyName=company.companyName,
                companyRepresentative=company.companyRepresentative,
                displayName=company.displayName,
                zipCode=company.zipCode,
                address1=company.address1,
                address2=company.address2,
                address3=company.address3,
                phoneNumber=company.phoneNumber,
                email=company.email,
                department=company.department,
                personInCharge=company.personInCharge,
                fax=company.fax,
                employeeCount=company.employeeCount,
                shopCount=company.shopCount,
                firstMonthOfTheYear=company.firstMonthOfTheYear,
                privacyPolicyType=company.privacyPolicyType,
                privacyPolicyContent=company.privacyPolicyContent
            )
            company_details.append(get_details)
            '''
            path = cm_api + 'company/'
            companyCode = company_code
            #response = await api_req(path, 'GET', jwt)
            null = None
            response = {"status_code": 200} # <-tedt用
            if response['status_code'] == 200: #response.status_code == 200:
                #resp_data = response.json()
                resp_data = {
                    "total": 70,
                    "resultsSize": 70,
                    "results": [
                        {
                          "privacyPolicyType": "0",
                          "prefecturesCode": "13",
                          "deleteFlag": 0,
                          "companyCode": "00000001",
                          "companyName": "株式会社ファーストグループ",
                          "address2": "2-11-5",
                          "address1": "渋谷区渋谷",
                          "insertAt": "2020-11-20 10:11:54",
                          "companyReservationUrl": "http://rebrand.ly/rm992w5",
                          "firstMonthOfTheYear": 202007,
                          "phoneNumber": "03-6803-8490",
                          "deleteId": null,
                          "deleteAt": null,
                          "email": "takaaki.todo@firstgroup.jp",
                          "updateAt": "2021-12-07 19:00:17",
                          "personInCharge": null,
                          "companyRepresentative": "藤堂 高明",
                          "id": 1,
                          "insertId": 1,
                          "zipCode": "150-0002",
                          "shopCount": 23,
                          "department": null,
                          "fax": null,
                          "updateId": 1044,
                          "employeeCount": 210,
                          "ownerStaffCode": "00000001",
                          "displayName": "株式会社ファーストグループ",
                          "address3": "",
                          "privacyPolicyContent": null
                        },
                        {
                          "privacyPolicyType": "0",
                          "prefecturesCode": "34",
                          "deleteFlag": 0,
                          "companyCode": "00000002",
                          "companyName": "株式会社くるま生活",
                          "address2": "2-9-25",
                          "address1": "福山市明神町",
                          "insertAt": "2020-11-20 10:11:54",
                          "companyReservationUrl": null,
                          "firstMonthOfTheYear": 202011,
                          "phoneNumber": "084-943-7123",
                          "deleteId": null,
                          "deleteAt": null,
                          "email": "",
                          "updateAt": "2020-11-20 10:11:54",
                          "personInCharge": null,
                          "companyRepresentative": "井上　康一",
                          "id": 2,
                          "insertId": 1,
                          "zipCode": "721-0961",
                          "shopCount": 1,
                          "department": null,
                          "fax": null,
                          "updateId": 1,
                          "employeeCount": 14,
                          "ownerStaffCode": "00000003",
                          "displayName": "株式会社くるま生活",
                          "address3": "",
                          "privacyPolicyContent": null
                        }
                    ]
                }
                results = resp_data["results"]
                check_company = [x['companyCode'] for x in results]
                if company_code not in check_company:
                    result = {"status_code": 204,
                              "result": company_code+" not found"}
                    return result
                for data in results:
                    if data["companyCode"] == company_code:
                        company_details = dict(
                            companyCode=data["companyCode"],
                            ownerStaffCode=data["ownerStaffCode"],
                            companyName=data["companyName"],
                            companyRepresentative=data["companyRepresentative"],
                            displayName=data["displayName"],
                            zipCode=data["zipCode"],
                            address1=data["address1"],
                            address2=data["address2"],
                            address3=data["address3"],
                            phoneNumber=data["phoneNumber"],
                            email=data["email"],
                            department=data["department"],
                            personInCharge=data["personInCharge"],
                            fax=data["fax"],
                            employeeCount=data["employeeCount"],
                            shopCount=data["shopCount"],
                            firstMonthOfTheYear=data["firstMonthOfTheYear"],
                            privacyPolicyType=data["privacyPolicyType"],
                            privacyPolicyContent=data["privacyPolicyContent"]
                        )
                        logging.debug(
                            "SP consol API | company_details:{}".format(company_details))
                        return company_details

        except Exception as e:
            logging.error(
                    'SP console API | get_sp_details():{}'.format(e))
            return False


#test用 cM API company
def get_cm_company(db, claims):
    if claims:
        try:
            company = db.query(CompanyTable).all()
            company_details = []
            for i in range(len(company)):
                get_company = dict(
                    companyCode=company[i].companyCode,
                    ownerStaffCode=company[i].ownerStaffCode,
                    companyName=company[i].companyName,
                    companyRepresentative=company[i].companyRepresentative,
                    displayName=company[i].displayName,
                    zipCode=company[i].zipCode,
                    address1=company[i].address1,
                    address2=company[i].address2,
                    address3=company[i].address3,
                    phoneNumber=company[i].phoneNumber,
                    email=company[i].email,
                    department=company[i].department,
                    personInCharge=company[i].personInCharge,
                    fax=company[i].fax,
                    employeeCount=company[i].employeeCount,
                    shopCount=company[i].shopCount,
                    firstMonthOfTheYear=company[i].firstMonthOfTheYear,
                    privacyPolicyType=company[i].privacyPolicyType,
                    privacyPolicyContent=company[i].privacyPolicyContent
                )
                company_details.append(get_company)
            return company_details
        except Exception as e:
            logging.error(
                    'SP console API | get_sp_details():{}'.format(e))
            return False


#add
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


# add register
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
            phone_numbe=sp_info.storeInfos[i].phoneNumber
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
        print(sp_info.staffInfos[i].staffRoleName)
        role = staff_code[role_name]
        id_check = sp_info.staffInfos[i].userId
        cognito_pass = sp_info.staffInfos[i].password
        if(re.fullmatch(regex, id_check)):
            logging.debug('Email format:{}'.format(id_check))
            print(os.environ['cognito_password'])
            user_pool = os.environ['staff_userpool_id']
            checked_email = id_check
            checked_user_name = ""
        else:
            logging.debug('User name format:{}'.format(id_check))
            user_pool = os.environ['username_userpool_id']
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
                    filter(SequenceTable.types == company_category).first()
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
                    ssl_arn = os.environ['lotas_ssl_arn']
                    zone_id = os.environ['lotas_zone_id']
                else:
                    ssl_arn = os.environ['domain_ssl_arn']
                    zone_id = os.environ['zone_id']

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
                                "schema_name": os.environ['schema_name'],
                                "api_userpool_id":
                                os.environ['api_userpool_id'],
                                "staff_userpool_id":
                                os.environ['staff_userpool_id'],
                                "username_userpool_id":
                                os.environ['username_userpool_id'],
                                "carsSERVICE_password":
                                os.environ['carsSERVICE_password'],
                                "DIC_api_password":
                                os.environ['DIC_api_password'],
                                "survey_password":
                                os.environ['survey_password'],
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
                                "address1": sp_info.companyInfo.building,
                                "address2": sp_info.companyInfo.address,
                                "address3": "",
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
                    bucket = os.environ['bucket_name']
                    folder = 'test'
                    file_name = trans_num+'.json'
                    key = folder+'/'+file_name
                    result = upload_json(bucket, key, json_data)
                    if result:
                        try:
                            data = {}
                            data['fileName'] = key
                            data['status'] = 0
                            logging.debug('cM API path:{}'.format(data))
                            path = cm_api + 'addSpManagement/'+str(trans_num)
                            logging.debug('cM API path:{}'.format(path))
                            # connection to cM API[POST]
                            #response = await api_req(path, 'POST', jwt, data)
                            response = {"status_code": 200} # <-tedt用
                            if response['status_code'] == 200:#response.status_code == 200:
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
                                'SP console API | cM API error:{}'.format(e))
                            db_sp.rollback()
                            delete_json(bucket, key)
                            return False

                    else:
                        logging.error(
                            'SP console API | s3 error:{}'.format(result))
                        db_sp.rollback()
                        return False
                else:
                    logging.error(
                        'SP console API | json error:{}'.format(json_data))
                    return False

        except Exception as e:
            logging.error(
                    'SP console API | SP register failed:{}'.format(e))
            db_sp.rollback()
            return False
