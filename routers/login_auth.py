from fastapi import APIRouter, Depends
from jwks.auth_jwks import get_current_user
from starlette.responses import JSONResponse
from common.conn import get_sp_ro_db
from sqlalchemy.orm import Session
from controller.login_auth import user_auth

router = APIRouter()


@router.get("/auth/login")
async def login_auth(db_sp_ro: Session = Depends(get_sp_ro_db),
                     claims: str = Depends(get_current_user)):
    '''
    Login API
    :param jason_web_token[id_token]
    '''
    result = user_auth(db_sp_ro, claims)
    if result:
        return JSONResponse(
            status_code=200,
            content=dict(
                result="Authentication　success",
                user=result[0].userId,
                role=result[0].role))
    return JSONResponse(
        status_code=400,
        content=dict(
            result="Authentication　failed"))
