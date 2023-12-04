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

|  字段名   |            说明             |
| :-------: | :-------------------------: |
|  file_id  | 文件id，md5加密后的文件路径 |
| file_name |           文件名            |
| file_path |          文件路径           |





