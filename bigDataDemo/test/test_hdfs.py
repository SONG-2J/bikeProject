from bigDataDemo import config
from bigDataDemo import hdfsFun
from hdfs.client import Client

client = Client(url=config.HDFS_WEB, root=None, proxy=None, timeout=None, session=None)

if __name__ == '__main__':
    # 测试读取hdfs上的数据
    # data = hdfsFun.read_hdfs_file(client, '/home/sjj/hive/warehouse/ods.db/wash_info/wm_info.csv')
    # print(data)

    # 测试写入
    hdfsFun.write2hdfs(client, '/test/test.csv', '哈哈哈哈哈哈哈\n')

    # 测试追加
    hdfsFun.append2hdfs(client, '/test/test.csv', '呜呜呜呜呜呜呜\n')
