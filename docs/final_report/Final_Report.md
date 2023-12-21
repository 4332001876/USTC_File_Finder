# 大数据系统实验

## 组员名单及具体分工

- PB21030838 罗浩铭:负责整体框架的搭建，以及检索部分（包括传统查询数据库elastic search, 向量查询数据库milvus的搭建与交互），并完成了项目在云服务器上的部署，以及上台答辩
- PB21061199 范晨晓:负责爬虫部分（包括设置对不同网页的遍历方式控制），以及对网页数据的解析与存储，参与了与hbase数据库交互的工作
- PB21151807 刘海琳:负责hbase数据库的搭建与交互部分，前端搭建，以及答辩PPT制作


## 技术路线
### 概述
我们基于HBase, ElasticSearch, Milvus等框架及其Python API实现了一个文件查询系统，用于查找中科大各校内网站的在线文件。我们使用爬虫来从各个网站爬取各文件的标题、URL、日期、来源等信息，并将这些信息存储到HBase数据库中，同时在ElasticSearch搜索引擎与Milvus向量查询数据库建立查询索引。我们使用ElasticSearch来对文件的标题、来源等信息进行检索，同时使用Milvus来对文件标题的embedding进行向量查询以扩展搜索结果。最终我们使用gradio框架搭建了一个简单的前端，用于接收用户的查询请求，并美观地展示查询结果。网站已经在云服务器上部署，可以通过[USTC File Finder](http://47.76.73.185:7860/)来访问。

<img src="./pic/final_website.png" width="100%" style="margin: 0 auto;">

### 代码框架
源代码框架如下：

```txt
USTC_File_Finder
├── docs # 文档
├── src # 源代码
│   ├── crawler # 爬虫
│   ├── data_access # 数据库访问接口
│   ├── server # 后端
|   ├── config.py # 配置信息，整个项目的配置信息都在这里
|   ├── main.py # 项目入口
|   └── test.py # 测试代码，定义了一个Tester.py类，用于测试各个模块的功能
```

其中`crawler`包含了爬虫部分的代码，`data_access`包含了HBase数据库访问及ElasticSearch与Milvus查询的代码，`server`包含了前端及其所需后端逻辑的代码，`config.py`包含了整个项目的配置信息，`main.py`是项目的入口，`test.py`包含了测试代码，定义了一个`Tester.py`类，用于测试各个模块的功能。

### 爬虫
crawler文件夹下的文件结构为:
- crawler.py：爬虫功能函数，实现对网站结构数据web_list.json的读取，自动遍历所有网站的所有可见页码，将结果输出在csv文件中
- web_list.json：存储着所有网站的url、编码方式、翻页策略、名称以及结构信息，以便爬虫函数调用
- file_list.csv：爬虫函数完成读取后，输出的文件列表。包含文件url、名称、发布时间以及来源
- web_list.txt：前期调研时收集的网站数据，用于逐个分析网站html结构，人力构建web_list.json。共收集了91个网站的数据

<kbd>web_list.json</kbd>结构：
&emsp;&emsp;这个数据库中存储着所有网站的结构信息，这样，只需要通过一个统一的爬虫函数，就可以实现对不同的网站进行爬取。
&emsp;&emsp;以下是一项网站数据的内容示例。在这个数据库中，一共存储着91个这样的数据，以便于实现对网站文件内容的实时读取与刷新。
```json
{
    "url": "https://finance.ustc.edu.cn/xzzx/list{page_num}.psp",
    # 网站网址
    "encoding": null,
    # 有的网站需要指定'utf-8'编码方式
    "title": "财务处",
    # 该网站名称
    "dtype": null,
    # 有的网站有多个子文件列表，在此处存储一级文件列表名称
    "dtype2": null,
    # 有的网站有多个子文件列表，在此处存储二级文件列表名称
    "flip": true,
    # 标识该网站是否可翻页，可翻页的网站均在url中标识了翻页逻辑
    "html_locator": [
        # 用于定位文件列表，包含着若干个字典，每个字典对应一次定位操作
        {
            "method": "find",   # 定位所用方法
            "args": "ul",       # 定位对象
            "kwargs": {         # 可选的辅助定位参数
                "class_": "news_list list2"
            }
        },
        {
            "method": "find_all",
            "args": "li"
        }
    ],
    "info_locator": [
        # 得到文件列表后，对文件中的每一项对应的名称、url、时间进行定位。每个字典对应对一个对象进行定位
        {
            "info": "title",    # 定位对象
            "method": "find",   # 定位方法
            "args": "a",        # 定位对象的类型。可为字符串（不需要额外辅助定位参数），也可为字典（需要额外辅助定位参数）
            "args2": "text"     # 提取出对象的形式
        },
        {
            "info": "url",
            "method": "find",
            "args": "a",
            "args2": "href"
        },
        {
            "info": "time",
            "method": "find",
            "args": [
                "span",
                {
                    "class_": "news_meta"
                }
            ],
            "args2": "text"
        }
    ]
}
```


<kbd>crawler.py</kbd>函数：
&emsp;&emsp;在爬虫函数中，定义了一个爬虫类。类中有以下功能函数：
- <kbd>fetch_data</kbd>：通过指定的url和编码方式，读取网站html结构的文本信息
- <kbd>fetch_file</kbd>：从web_list.json获取出网站的结构信息，利用结构信息定位到文件所在的列表
- <kbd>get_info</kbd>：实现根据web_list.json中存储的内容对应结构信息，返回对应内容的文本
- <kbd>fetch_file_list</kbd>：调用fetch_file得到文件列表后，对列表中的项逐个遍历，利用web_list.json文件中所存储的各项内容的结构信息，读取出每个文件的url、时间、标题等内容，并对数据格式进行一定处理
- <kbd>generate_file_list</kbd>：对web_list.json中的每一项（每一项对应一个网站）进行读取，并对可以翻页的网站进行翻页遍历直至无法获取内容为止。调用fetch_file_list得到文件列表并返回
- <kbd>generate_file_csv</kbd>：将generate_file_list返回的文件列表写入csv文件中，以便下游数据库的接入

<kbd>file_list.csv</kbd>：
&emsp;&emsp;存储着爬取得到的文件信息。以下为内容示例：
|            title             |                                               url                                                |    time    |  source  | file_type | file_type_2 |
| :--------------------------: | :----------------------------------------------------------------------------------------------: | :--------: | :------: | :-------: | :---------: |
| 研究生教学研究项目立项申请书 | http://gradschool.ustc.edu.cn/static/upload/article/picture/786794f67b044809935173f9cbc44110.doc | 2020-03-10 | 研究生院 | 培养工作  |  教学研究   |


各个网站爬取的文件数量如下：
|          网站          | 文件数 |
| :--------------------: | :----: |
|         教务处         |  854   |
|        研究生院        |  253   |
|        软件学院        |  177   |
|     先进技术研究院     |  139   |
|      网络信息中心      |   91   |
|    国际合作与交流部    |   75   |
|        超算中心        |   71   |
|        学工在线        |   58   |
|    信息科学技术学院    |   43   |
|         出版社         |   39   |
|     苏州高等研究院     |   35   |
|    资产与后勤保障处    |   30   |
|   计算机科学技术学院   |   23   |
|    保卫与校园管理处    |   17   |
|    信息科学实验中心    |   16   |
| 科技成果转移转化办公室 |   15   |
|    网络空间安全学院    |   14   |
|       大数据学院       |   7    |
|      工程科学学院      |   7    |

我们在爬虫部分的技术路线亮点有：
- 通过json数据库存储所有网站的结构信息，数据可维护性好
- 使用统一的爬虫函数，代码整洁
- 可以实现自动遍历数据库中的所有网站，对文件信息进行更新
- 实现了自动翻页，一方面提升了文件内容、另一方面也使得网站结构数据库精简可阅读性好
- 解决了一些网站显示的bug，例如软件学院的网站文件时间有误（可能是发生过数据迁移导致的）。我们重新读取修正了时间数据




### hbase数据库
我们基于Python的happybase库，并借助HBase的Thrift服务，来实现我们的项目与HBase数据库之间的交互。

我们实现了一个`HbaseHelper`类，用来管理与HBase数据库之间的连接与增删改查操作。我们还实现了以我们项目定义的`FileRecord`文件信息类为API的数据库交互函数，包括将`FileRecord`对象存入HBase数据库或覆盖HBase数据库中原有条目的`put_file`函数，以及将HBase数据库中读出数据转换为`FileRecord`对象的`get_file`函数。

数据库内存储的内容结构如下：

在列族`info`中我们存储了如下文件信息：

|    列名     |          信息          |
| :---------: | :--------------------: |
|    title    |        文件标题        |
|     url     |        文件URL         |
|    time     |      文件发布时间      |
|   source    |        文件来源        |
|  file_type  | 文件在网站中的一级类型 |
| file_type_2 | 文件在网站中的二级类型 |

在列`counter:increment_id`的`row_increment_id`行中我们存储了一个HBase的自增计数器，用于将row_key命名为`f'row_{increment_id}'`，这将保证各文件的row_key不同，同时这些row_key将用来关联HBase数据库与其它查询数据库。



### elastic search
由于HBase对搜索功能几乎没有支持，因此我们使用ElasticSearch来对文件的标题、来源等信息进行检索。Elasticsearch是一个分布式、RESTful风格的搜索和数据分析引擎，支持分词查询、模糊查询、查询结果排序，非常适用于当前文本查询的场景。由于其原生支持分布式部署，因此可以保证我们项目的可扩展性。
我们使用Python的ElasticSearch库来实现我们的项目与ElasticSearch搜索引擎之间的交互。

我们实现了`ElasticsearchHelper`类，用来管理ElasticSearch的连接及增删改查操作。

搜索结果以row_key的形式与原HBase数据库关联。


### milvus数据库
在尝试传统查询框架的同时，我们也尝试了向量查询框架。我们使用Milvus向量查询数据库来对文件标题的embedding进行向量查询以扩展搜索结果。
Milvus 是一个云原生的向量数据库，具有以下特点：
高性能：性能高超，完成万亿条向量数据搜索的平均延迟以毫秒计
高可用、高可靠、高可扩展性：支持分布式部署，具有高容错容灾能力
功能强大：增量数据摄取、标量向量混合查询、time travel 等

由于其原生支持分布式部署，因此可以保证我们项目的可扩展性。

我们实现了`TitleToVec`类，使用Hugging Face上最热门的中文BERT模型`bert-base-chinese`预训练模型对文件标题及查询关键词生成embedding。对每一个标题用BERT处理，并以BERT的`pooler output`（`[cls]` token对应位置的输出token，包含了整个句子的语义信息）作为标题的sentence embedding。我们以该标题的embedding作为Milvus向量查询数据库的索引。查询时，同样用BERT生成查询关键词的embedding，作为查询向量，来对文件标题进行向量查询。

搜索结果以row_key的形式与原HBase数据库关联。


### 搜索引擎管理
我们实现了一个`SearchEngine`类，用来ElasticSearch与Milvus向量数据库的查询，整合多来源的查询结果，并以查询得到的条目的row_key从HBase数据库中读出数据。

### 前端
我们使用了gradio框架搭建了一个简单的前端，用于接收用户的查询请求，并美观地展示查询结果。


网站已经在云服务器上部署，其网址为：http://47.76.73.185:7860/
欢迎大家访问和体验！

## 实现功能介绍




## 核心代码块
实验报告要求的


## 组员总结与心得
### 罗浩铭
我实现了

在这次实验中，我磨练了我使用各大数据框架的技术，提高了我对大数据系统特别是搜索引擎等技术的理解。相信在数据处理需求日益

### 范晨晓



### 刘海琳
