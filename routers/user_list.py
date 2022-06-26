import logging
from models.model import UsersTable


def role_list(db, claims):
    if claims:
        try:
            users_list = db.query(UsersTable).all()
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
