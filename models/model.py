from sqlalchemy import Column, Integer, String, DateTime, func
from common.conn import Base_SP
from pydantic import BaseModel


class UsersTable(Base_SP):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    role = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=func.utc_timestamp())
    updated_at = Column(DateTime, default=func.utc_timestamp(),
                        onupdate=func.utc_timestamp())
    cognitoId = Column(Integer, nullable=True)


class UserRegister(BaseModel):
    email: str
    name: str
    pw: str


class EditUser(BaseModel):
    id: int
    pw: str
    role: int
