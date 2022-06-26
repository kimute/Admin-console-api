from fastapi import FastAPI
from routers import login_auth, user_list, crud_user, sp_list, health_check
from starlette.middleware.cors import CORSMiddleware
from common.consts import origins


def create_app():
    app = FastAPI(
        title="SP console API", desciption="SP admin Console API", version="1.0.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(health_check.router, prefix="/api/v1")
    app.include_router(
        login_auth.router, tags=["Authentication"], prefix="/api/v1")
    app.include_router(
        user_list.router, tags=["Users Info"], prefix="/api/v1")
    app.include_router(
        crud_user.router, tags=["Users Info"], prefix="/api/v1")
    app.include_router(sp_list.router, tags=["SP"], prefix="/api/v1")
    return app


app = create_app()
