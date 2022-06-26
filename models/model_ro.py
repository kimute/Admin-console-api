from sqlalchemy import Column, Integer, String, DateTime, func
from common.conn import Base_SP_ro


class UsersTable_ro(Base_SP_ro):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    role = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=func.utc_timestamp())
    updated_at = Column(DateTime, default=func.utc_timestamp(),
                        onupdate=func.utc_timestamp())
    cognitoId = Column(Integer, nullable=True)
