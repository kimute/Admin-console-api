import os
import requests
import logging
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from starlette.status import HTTP_403_FORBIDDEN
from jwks.jwt_plugin import JWKS, JWTBearer, JWTAuthorizationCredentials

load_dotenv()
region = os.getenv('REGION')
userpool_id = os.getenv('USERPOOLID')
keys_url = 'https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json'.format(region, userpool_id)

jwks = JWKS.parse_obj(
    requests.get(
        keys_url
    ).json()
)

auth = JWTBearer(jwks)


async def get_current_user(
        credentials: JWTAuthorizationCredentials = Depends(auth)) -> str:
    try:
        return credentials.claims
    except KeyError:
        logging.error(
                'sp console API | get_current_user:{}'.format(KeyError))
        HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="missing user")


async def get_jwt(
        credentials: JWTAuthorizationCredentials = Depends(auth)) -> str:
    try:
        return credentials.jwt_token
    except KeyError:
        logging.error(
                'sp console API | get_current_user:{}'.format(KeyError))
        HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="missing user")
