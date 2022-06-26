from sqlalchemy import (
    Column, Integer, String, DateTime,Text, func)
from common.conn import Base_SP
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional


class SpInfoTable(Base_SP):
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


class companyInfo(BaseModel):
    address: str
    building: Optional[str] = None
    companyCategory: str
    companyName: str
    contractEndDate: str
    contractStartDate: str
    domain: str
    email: str
    employeeCount: str
    externalSystem: str
    firstMonthOfTheYear: str
    maxStaff: str
    maxStore: str
    municipalities: str
    oemType: str
    ownerName: str
    phoneNumber: str
    prefectures: str
    storeCount: str
    subDomain: str
    zipCode: str
    honbuCode: Optional[str] = None


class storeInfo(BaseModel):
    address: str
    building: str
    externalSystemStoreName: str
    municipalities: str
    phoneNumber: Optional[str] = None
    prefectures: str
    storeName: str
    zipCode: Optional[str] = None


class staffInfo(BaseModel):
    externalSystemStoreName: List[str] = []
    firstNameFurigana: str
    firstNameKanji: str
    jobCategory: str
    lastNameFurigana: str
    lastNameKanji: str
    password: str
    staffRoleName: str
    userId: str


class spInfo(BaseModel):
    companyInfo: companyInfo
    storeInfos: List[storeInfo]
    staffInfos: List[staffInfo]
