import os
import logging
import requests
import boto3
import json
from aws_xray_sdk.core import patch_all

logging.basicConfig(level=logging.WARN)
patch_all()

USER_POOL_ID = os.environ['USER_POOL_ID']
PREFERRED_USERNAME_USER_POOL_ID = os.environ['PREFERRED_USERNAME_USER_POOL_ID']
CARS_MANAGEMENT_USER_POOL_ID = os.environ['CARS_MANAGEMENT_USER_POOL_ID']
CLIENT_ID = os.environ['CLIENT_ID']
COMPANY_CODE = os.environ['COMPANY_CODE']
USERNAME = os.environ['USERNAME']
PASSWORD = os.environ['PASSWORD']
API_ENDPOINT = os.environ['CARS_MANAGEMENT_API_ENDPOINT']
REQUEST_TIMEOUT = 30
cognito = boto3.client('cognito-idp')


def lambda_handler(event, context):

    try:
        # not sign in user
        if 'request' in event:
            if 'userNotFound' in event['request']:
                if event['request']['userNotFound']:
                    return event

        # user name check
        userPoolId = event['userPoolId']
        userName = event['userName']
        if userName == USERNAME:
            return event
        if userPoolId != USER_POOL_ID and userPoolId != PREFERRED_USERNAME_USER_POOL_ID: 
            logging.error("User pool ID is different ")
            raise Exception(f"Authentication Error User Pool ID is different。:{userPoolId}")

        # Get token for API request
        auth = cognito.admin_initiate_auth(
            UserPoolId=CARS_MANAGEMENT_USER_POOL_ID,
            ClientId=CLIENT_ID,
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                'USERNAME': USERNAME,
                'PASSWORD': PASSWORD,
            }
        )
        idToken = auth['AuthenticationResult']['IdToken']

        if userPoolId == USER_POOL_ID:
            email = event['request']['userAttributes']['email']
            # Contract Status Retrieval API 
            res = requests.get(
                f'{API_ENDPOINT}/v1/userpool/{userPoolId}/email/{email}/contractstatus', 
                headers={
                    'authorization': f"Bearer {idToken}",
                },
                timeout=REQUEST_TIMEOUT,
            )
        elif userPoolId == PREFERRED_USERNAME_USER_POOL_ID:
            preferredUsername = event['request']['userAttributes']['preferred_username'] 
            # Contract Status Retrieval API 
            res = requests.get(
                f'{API_ENDPOINT}/v1/userpool/{userPoolId}/preferredUsername/{preferredUsername}/contractstatus',  # noqa: E501
                headers={
                    'authorization': f"Bearer {idToken}",
                },
                timeout=REQUEST_TIMEOUT,
            )
        if res.status_code != requests.codes.ok:
            logging.error("request failed")
            res.raise_for_status()
        else:
            body = res.json()
            # Contract Status Check
            if not body.get("isContract"):
                logging.error("contract not found")
                raise Exception(
                    f"Authentication error no contract found. User Pool ID:{userPoolId} email:{email}")  
            # Contract Status Check
            if not body.get("isUserStatus"):
                logging.error("ユーザステータス異常")
                raise Exception(
                    f"Authentication error no contract found:{userPoolId} email:{email}")  
    except Exception as err:
        eventJson = json.dumps(event)
        logging.error(f"event:{eventJson}", exc_info=err)
        raise err

    return event