from sqlalchemy import (
    Column, Integer, String, DateTime,Text, func)
from common.conn import Base_SP_ro


class SequenceTable_ro(Base_SP_ro):
    __tablename__ = 'sequence_manager'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column('type', String(13))
    value = Column('value', String(255))
