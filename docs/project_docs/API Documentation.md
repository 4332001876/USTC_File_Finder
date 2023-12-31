# API文档

## 项目结构

```txt
USTC_File_Finder
├── docs # 文档
│   ├── project_docs # 项目文档
│   │   ├── API Documentation.md 
│   │   ├── Deployment Document.md
│   │   ├── Design Document.md
│   │   └── Requirement Document.md
│   └── survey_docs # 调研文档，用于记录学习到的项目需要的知识，以及python库的使用方法等
├── src # 源代码
│   ├── server # 后端
│   ├── data_access # 数据库访问接口
│   ├── crawler # 爬虫
├── config.py # 配置信息，整个项目的配置信息都在这里
├── main.py # 项目入口
└── test.py # 测试代码，定义了一个Tester.py类，用于测试各个模块的功能
```

## 数据库结构

- 在列族`info`中我们存储了如下文件信息：

|    列名     |          信息          |
| :---------: | :--------------------: |
|    title    |        文件标题        |
|     url     |        文件URL         |
|    time     |      文件发布时间      |
|   source    |        文件来源        |
|  file_type  | 文件在网站中的一级类型 |
| file_type_2 | 文件在网站中的二级类型 |

- 在列`counter:increment_id`的`row_increment_id`行中我们存储了一个HBase的自增计数器，用于将row_key命名为`f'row_{increment_id}'`，这将保证各文件的row_key不同，同时这些row_key将用来关联HBase数据库与其它查询数据库。

其它框架检索结果以rowkey与HBase数据库中的rowkey进行关联，从而获取文件的详细信息。


