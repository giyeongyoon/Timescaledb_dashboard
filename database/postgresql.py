# dashboard/database/postgresql.py
import psycopg2
import time
from common.consts import db_info
import logging

logger = logging.getLogger(__name__)

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
            logger.info("DB 연결 성공공")
            return conn
        except Exception as e:
            logger.warning(f"[{i+1}/{retries}] DB 연결 실패: {e}")
            time.sleep(delay)

    
    logger.critical("모든 DB 연결 시도도 실패")
    raise Exception("DB 연결 실패")
