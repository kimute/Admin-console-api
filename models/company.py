from sqlalchemy import (
    Column, Integer, String, DateTime,Text, func)
from common.conn import Base_SP
from datetime import datetime


class CompanyTable(Base_SP):
    __tablename__ = 'company'
    id = Column(Integer, primary_key=True, autoincrement=True)
    companyCode = Column('company_code', String(13))
    ownerStaffCode = Column('owner_staff_code', String(13), nullable=True)
    companyName = Column('company_name', String(255), nullable=True)
    companyRepresentative = Column(
        'company_representative', String(255), nullable=True)
    displayName = Column('display_name', String(255), nullable=True)
    zipCode = Column('zip_code', String(255), nullable=True)
    prefecturesCode = Column('prefectures_code', String(13), nullable=True)
    address1 = Column('address1', String(255), nullable=True)
    address2 = Column('address2', String(255), nullable=True)
    address3 = Column('address3', String(255), nullable=True)
    phoneNumber = Column('phone_number', String(255), nullable=True)
    email = Column('email', String(255), nullable=True)
    department = Column('department', String(255), nullable=True)
    personInCharge = Column('person_in_charge', String(255), nullable=True)
    fax = Column('fax', String(255), nullable=True)
    employeeCount = Column('employee_count', Integer, nullable=True)
    shopCount = Column('shop_count', Integer, nullable=True)
    firstMonthOfTheYear = Column(
        'first_month_of_the_year', Integer, nullable=True)
    privacyPolicyType = Column('privacy_policy_type', String(1), nullable=True)
    privacyPolicyContent = Column(
        'privacy_policy_content', Text, nullable=True)
    companyReservationUrl = Column(
        'company_reservation_url', String(255), nullable=True)
    insertId = Column('insert_id', Integer)
    insertAt = Column('insert_at', DateTime)
    updateId = Column('update_id', Integer)
    updateAt = Column('update_at', DateTime)
    deleteId = Column('delete_id', Integer, nullable=True)
    deleteAt = Column('delete_at', DateTime, nullable=True)
    deleteFlag = Column('delete_flag', Integer)
