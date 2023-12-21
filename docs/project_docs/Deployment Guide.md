# 部署指南

本项目需要在hbase服务、ElasticSearch服务与milvus服务开启的情况下运行

## 启动milvus服务
在docker开启的情况下，运行以下命令启动milvus服务
```bash
cd <project_path>/env/milvus
docker-compose up -d
```

若容器已构建，可直接运行`docker start [OPTIONS] CONTAINER [CONTAINER...]`命令启动milvus服务

## 启动ElasticSearch服务
同上，启动ElaticSearch的docker容器

## 配置Hbase
除常规配置外，需要在hbase-site.xml中添加以下配置
```xml
<property>
  <name>hbase.regionserver.thrift.address</name>
  <value>0.0.0.0</value>
</property>
<property>
  <name>hbase.regionserver.thrift.port</name>
  <value>9090</value>
</property>
<property>
  <name>hbase.regionserver.thrift.http</name>
  <value>true</value>
</property>
<property>
  <name>hbase.thrift.server.socket.read.timeout</name>
  <value>0</value>
</property>
```

特别是`hbase.thrift.server.socket.read.timeout`必须设置为0，否则超过一定时间（默认60s）没有对hbase数据库进行操作后，HBase的Thrift服务会自动断开连接，从而Python端会出现`TTransportException(type=4, message='TSocket read 0 bytes')`错误(参考github中的issue:https://github.com/python-happybase/happybase/issues/130)。

## 启动hbase服务
```bash
start-all.sh
start-hbase.sh
hbase-daemon.sh start thrift -p 9090 --infoport 9091
```

## 运行项目
```bash
cd <project_path>/src
nohup python3 main.py >/dev/null 2>&1 &
```