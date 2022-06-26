import logging
from models.model_ro import UsersTable_ro


def role_list(db_sp_ro, claims):
    if claims:
        try:
            users_list = db_sp_ro.query(UsersTable_ro).all()
            user_lists = []
            for i in range(len(users_list)):
                users = dict(
                    role=users_list[i].role,
                    name=users_list[i].name,
                    userId=users_list[i].userId, id=users_list[i].id)
                user_lists.append(users)
            return user_lists
        except Exception as e:
            logging.error(
                    'SP console API | role_list:{}'.format(e))
            return False
