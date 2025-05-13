import psycopg2
import time

POSTGRES_HOST = 'localhost'
conn = None

def connect_db():
    return psycopg2.connect(
        host=POSTGRES_HOST,
        port='5432',
        user='postgres',
        password='ygy@2628',
        dbname='blueberry'
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
