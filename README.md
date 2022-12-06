HDFS、Kafka、Storm、Spark、Hive、HBase、SpringBoot、ECharts、Superset、Mysql、MongoDB、Redis等

## 数据源

美国华盛顿共享单车使用量数据集

http://www.idatascience.cn/dataset-detail?table_id=22

北京公共交通数据集

http://www.idatascience.cn/dataset-detail?table_id=402

电信用户数据集

http://www.idatascience.cn/dataset-detail?table_id=206

国家幸福指数报告数据集

http://www.idatascience.cn/dataset-detail?table_id=100191

网页广告数据集

http://www.idatascience.cn/dataset-detail?table_id=435

非洲国家金融危机数据集

http://www.idatascience.cn/dataset-detail?table_id=14

新冠疫情

http://www.idatascience.cn/dataset-detail?table_id=100196

煤炭

http://www.idatascience.cn/dataset-detail?table_id=33

中国租房

http://www.idatascience.cn/dataset-detail?table_id=100086

年龄结构抚养比例

http://www.idatascience.cn/dataset-detail?table_id=100249

## Flume

```she
vim bike.conf
```

```properties
# Name the components on this agent
a1.sources = r1
a1.sinks = k1
a1.channels = c1

# Describe/configure the source
a1.sources.r1.type = exec
a1.sources.r1.command = tail -F /home/sjj/flume_data/bikeInfo/bike.csv

# Describe the sink
a1.sinks.k1.type = org.apache.flume.sink.kafka.KafkaSink
a1.sinks.k1.kafka.topic = test
a1.sinks.k1.kafka.bootstrap.servers = test:9092

# Use a channel which buffers events in memory
a1.channels.c1.type = memory
a1.channels.c1.capacity = 1000
a1.channels.c1.transactionCapacity = 100

# Bind the source and sink to the channel
a1.sources.r1.channels = c1
a1.sinks.k1.channel = c1
```

```shell
flume-ng agent -c $FLUME_HOME/conf/ -f bike.conf -n a1 -Dflume.root.logger=INFO,console
```

## Kafak

```shell
# 启动zookeeper
$KAFKA_HOME/bin/zookeeper-server-start.sh $KAFKA_HOME/config/zookeeper.properties

# 启动kafka
$KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties

# 创建topic
$KAFKA_HOME/bin/kafka-topics.sh --create --topic test --partitions 3 --replication-factor 1 --bootstrap-server test:9092 

# 生产者
$KAFKA_HOME/bin/kafka-console-producer.sh --topic test --broker-list test:9092

# 消费者
$KAFKA_HOME/bin/kafka-console-consumer.sh --topic test --from-beginning --bootstrap-server test:9092
```

## Hive

```shell
hive --service hiveserver &
```

```xml
  <property>
    <name>hive.server2.thrift.host</name>
    <value>test</value>
  </property>  
  <property>
    <name>hive.server2.thrift.port</name>
    <value>10000</value>
  </property>
  <property>
    <name>hive.server2.authentication</name>
    <value>NOSASL</value>
  </property>
  <property>
    <name>hive.auto.convert.join</name>
    <value>false</value>
  </property>
```

```hive
create database bike;
use bike;

create table bike(
  instant int,
  dteday string,
  season int,
  yr int,
  mnth int,
  holiday int,
  weekday int,
  workingday int,
  weathersit int,
  temp float,
  atemp float,
  hum float,
  windspeed float,
  casual int,
  registered int,
  cnt int)
  row format delimited fields terminated by ',';

alter table bike set TBLPROPERTIES ('skip.header.line.count'='1');


load data local inpath '/home/sjj/flume_data/bikeInfo/bike.csv' overwrite into table bike;
```

## 错误集锦

```shell
kafka.errors.UnsupportedCodecError: UnsupportedCodecError: Libraries for snappy compression codec not found

# 没安装必要的包snappy
pip3 install python-snappy
```

```shell
Caused by: com.mysql.cj.jdbc.exceptions.MysqlDataTruncation: Data truncation: Incorrect string value: '\xE4\xBB\xA5\xE4\xB8\x8A' for column 

将数据库编码设置为utf8，或者不要在视图字段中出现中文
```

