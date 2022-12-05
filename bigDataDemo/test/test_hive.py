from bigDataDemo import config
from pyhive import hive

hive_conn = conn = hive.connect(host=config.HOST_NAME,  # 主机
                                port=config.HIVE_PORT,  # hive端口
                                auth=config.HIVE_AUTH,
                                database=config.HIVE_DATABASE,  # 数据库
                                )
cursor = hive_conn.cursor()

if __name__ == '__main__':
    cursor.execute("show tables")
    print(cursor.fetchall())

    cursor.close()
