# 部署指南

本项目需要在hbase服务、ElasticSearch服务与milvus服务开启的情况下运行

## 启动milvus服务
在docker开启的情况下，运行以下命令启动milvus服务
```bash
cd <project_path>/env/milvus
docker-compose up -d
```

若容器已构建，可直接运行`docker start [OPTIONS] CONTAINER [CONTAINER...]`命令启动milvus服务