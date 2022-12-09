# 连接mysql
import pymysql

HOST = 'test'
PORT = 3306
USER = 'root'
PASSWORD = '123456'
DB = 'bike'
CHARSET = 'utf8'


def connMysql():
    conn = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, db=DB, charset=CHARSET)
    return conn
