'''
from sqlalchemy import (
    Column, Integer, String, DateTime, func)
from pydantic import BaseModel
from common.conn import Base
from common.conn import ENGINE
from typing import List, Optional, Set
from datetime import datetime, timezone


class Cognito(Base):
    __tablename__ = 'cognito'

    id = Column(Integer, primary_key=True, autoincrement=True)
    userPoolId = Column('user_pool_id', String(255))
    email = Column('email', String(255), nullable=True)
    preferredUsername = Column('preferred_username',
                               String(255), nullable=True)
    roleName = Column('role_name', String(255))
    lastLoginAt = Column('last_login_at', DateTime, nullable=True)
    verifyCode = Column('verify_code', String(255), nullable=True)
    verifyMail = Column('verify_mail', String(255), nullable=True)
    verifyExpiration = Column('verify_expiration', DateTime, nullable=True)
    status = Column('status', String(2), nullable=True)
    companyCode = Column('company_code', String(13), nullable=True)
    userCode = Column('user_code', String(13), nullable=True)
    insertId = Column('insert_id', Integer)
    insertAt = Column('insert_at', DateTime,
                      default=datetime.now(timezone.utc))
    updateId = Column('update_id', Integer)
    updateAt = Column('update_at', DateTime, default=datetime.now(
        timezone.utc), onupdate=datetime.now(timezone.utc))
    deleteId = Column('delete_id', Integer, nullable=True)
    deleteAt = Column('delete_at', DateTime, nullable=True)
    deleteFlag = Column('delete_flag', Integer, default=0)
'''