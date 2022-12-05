import config
import hdfsFun
from kafka import KafkaConsumer
from hdfs.client import Client

# kafka配置
consumer = KafkaConsumer(config.KAFKA_TOPIC,
                         bootstrap_servers=config.KAFKA_SERVER,
                         group_id='test-kafka',
                         auto_offset_reset='earliest',
                         value_deserializer=lambda m: m.decode('utf-8'))

# hdfs客户端配置
client = Client(url=config.HDFS_WEB, root=None, proxy=None, timeout=None, session=None)
# 写入文件路径
file_path = '/test/test.csv'

if __name__ == '__main__':
    hdfsFun.write2hdfs(client, file_path, '')
    for msg in consumer:
        v = msg.value
        if len(v) > 0:
            print(msg.value)
            # 写入hdfs
            hdfsFun.append2hdfs(client, file_path, v + '\n')
