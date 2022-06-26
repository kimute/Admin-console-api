import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from common import config
from dotenv import load_dotenv

load_dotenv()

#DB = os.getenv('DATABASE_URL')
#DB_RO = os.getenv('DATABASE_RO_URL')
DB_SP = os.getenv('DATABASE_SP_URL')
DB_SP_RO = os.getenv('DATABASE_SP_RO_URL')

#ENGINE = create_engine(
#    DB,
#    encoding="utf-8",
#    echo=True
#)
#
#ENGINE_RO = create_engine(
#    DB_RO,
#    encoding="utf-8",
#    echo=True
#)

ENGINE_SP = create_engine(
    DB_SP,
    encoding="utf-8",
    echo=True,
    pool_pre_ping=True
)

ENGINE_SP_RO = create_engine(
    DB_SP_RO,
    encoding="utf-8",
    echo=True,
    pool_pre_ping=True
)

#db_session = scoped_session(
#    sessionmaker(
#        autocommit=False,
#        autoflush=False,
#        bind=ENGINE
#    )
#)
#
#db_ro_session = scoped_session(
#    sessionmaker(
#        autocommit=False,
#        autoflush=False,
#        bind=ENGINE_RO
#    )
#)

db_sp_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=ENGINE_SP
    )
)

db_sp_ro_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=ENGINE_SP_RO
    )
)


#def get_db():
#    db = db_session()
#    try:
#        yield db
#    finally:
#        db.close()
#
#
#def get_ro_db():
#    db = db_ro_session()
#    try:
#        yield db
#    finally:
#        db.close()


def get_sp_db():
    db = db_sp_session()
    try:
        yield db
    finally:
        db.close()


def get_sp_ro_db():
    db = db_sp_ro_session()
    try:
        yield db
    finally:
        db.close()


#Base = declarative_base()
#Base.query = db_session.query_property()
#
#Base_ro = declarative_base()
#Base_ro.query = db_ro_session.query_property()

Base_SP = declarative_base()
Base_SP.query = db_sp_session.query_property()

Base_SP_ro = declarative_base()
Base_SP_ro.query = db_sp_ro_session.query_property()
