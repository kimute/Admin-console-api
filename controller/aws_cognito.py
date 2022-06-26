import os
import logging
from dotenv import load_dotenv
import boto3

load_dotenv()

region = os.getenv('REGION')
key_id = os.getenv('DB_USER')
access_key = os.getenv('ACCESS_KEY_ID')
secret_key = os.getenv('SECRET_ACCESS_KEY')
userPoolId = os.getenv('USERPOOLID')


def cognito_auth(email, password):
    try:
        cognito = boto3.client('cognito-idp',
                               region_name=region,
                               aws_access_key_id=access_key,
                               aws_secret_access_key=secret_key)

        cognito.admin_create_user(
                UserPoolId=userPoolId,
                Username=email,
                MessageAction="SUPPRESS",
                UserAttributes=[
                    {
                        'Name': "preferred_username",
                        'Value': email
                    }
                ],
            )

        cognito.admin_set_user_password(
            UserPoolId=userPoolId,
            Username=email,
            Password=password,
            Permanent=True
        )
        return True
    except Exception as e:
        logging.error('sp console API | cognito_auth failed:{}'.format(e))
        return False


def cognito_reset_pass(email, password):
    try:
        cognito = boto3.client('cognito-idp',
                               region_name=region,
                               aws_access_key_id=access_key,
                               aws_secret_access_key=secret_key)

        cognito.admin_set_user_password(
            UserPoolId=userPoolId,
            Username=email,
            Password=password,
            Permanent=True
        )
        return True
    except Exception as e:
        logging.error('sp console API | password change failed:{}'.format(e))
        return False


def cognito_delete(email):
    try:
        cognito = boto3.client('cognito-idp',
                               region_name=region,
                               aws_access_key_id=access_key,
                               aws_secret_access_key=secret_key)

        cognito.admin_delete_user(
            UserPoolId=userPoolId,
            Username=email
        )
        return True
    except Exception as e:
        logging.error('sp console API | user delete failed:{}'.format(e))
        return False


def upload_json(bucket, key, body):
    try:
        s3_client = boto3.client('s3',
                                 region_name=region,
                                 aws_access_key_id=access_key,
                                 aws_secret_access_key=secret_key)
        s3_client.put_object(Bucket=bucket, Key=key, Body=body)
        return True
    except Exception as e:
        logging.error('sp console API | upload json to s3 failed:{}'.format(e))
        return False


def delete_json(bucket, delete_key):
    try:
        s3_client = boto3.client('s3',
                                 region_name=region,
                                 aws_access_key_id=access_key,
                                 aws_secret_access_key=secret_key)
        s3_client.delete_object(Bucket=bucket, Key=delete_key)
        return True
    except Exception as e:
        logging.error('sp console API | delete json failed:{}'.format(e))
        return False
