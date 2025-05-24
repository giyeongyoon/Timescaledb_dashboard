# dashboard/database/postgresql.py
import psycopg2
import time
from common.consts import db_info

conn = None

def connect_db():
    return psycopg2.connect(
        host=db_info.get('host'),
        port=db_info.get('port'),
        user=db_info.get('user'),
        password=db_info.get('password'),
        dbname=db_info.get('dbname')
    )

def get_conn_db(retries=3, delay=2):
    for i in range(retries):
        try:
            conn = connect_db()
            print("DB 연결")
            return conn
        except:
            time.sleep(delay)

    if not conn:
        raise Exception("DB 연결 실패")
