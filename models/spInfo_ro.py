from sqlalchemy import (
    Column, Integer, String, DateTime,Text, func)
from common.conn import Base_SP_ro
from datetime import datetime


class SpInfoTable_ro(Base_SP_ro):
    __tablename__ = 'sp_info'

    id = Column(Integer, primary_key=True, autoincrement=True)
    companyCode = Column('company_code', String(13))
    companyName = Column('company_name', String(255), nullable=True)
    oem = Column('OEM', String(255), nullable=True)
    spUrl = Column('sp_url', String(255), nullable=True)
    insertAt = Column('insert_at', DateTime)
    updateAt = Column('update_at', DateTime)
    deleteAt = Column('delete_at', DateTime, nullable=True)
    deleteFlag = Column('delete_flag', Integer, default=0)
    status = Column('status', Integer, nullable=True)
