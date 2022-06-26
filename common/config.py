import os
from dotenv import load_dotenv

load_dotenv()

# SQLAlchemy接続情報の設定(local用)
SQLALCHEMY_DATABASE_URI = \
    'mysql+pymysql://{user}:{password}@db:{port}/{db_name}?charset=utf8'\
    .format(**{
            'user': os.getenv('DB_USER'),
            'password': os.getenv('MYSQL_ROOT_PASSWORD'),
            'host': os.getenv('DB_HOST'),
            'port': int(os.getenv('DB_PORT')),
            'db_name': os.getenv('DB_DATABASE')
    })