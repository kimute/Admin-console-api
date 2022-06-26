import logging
from models.model_ro import UsersTable_ro


def user_auth(db_sp_ro, claims):
    if claims:
        user = claims["email"]
        try:
            users_info = db_sp_ro.query(UsersTable_ro).\
                filter(UsersTable_ro.userId == user).all()
            return users_info
        except Exception as e:
            logging.error(
                    'SP console API | user_auth:{}'.format(e))
            return False
