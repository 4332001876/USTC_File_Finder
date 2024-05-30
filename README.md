# USTC_File_Finder

我们基于HBase, ElasticSearch, Milvus等框架及其Python API实现了一个文件查询系统，用于查找中科大各校内网站的在线文件。我们使用爬虫来从各个网站爬取各文件的标题、URL、日期、来源等信息，并将这些信息存储到HBase数据库中，同时在ElasticSearch搜索引擎与Milvus向量查询数据库建立查询索引，以便用户以关键词检索文件标题。我们使用ElasticSearch来对文件的标题、来源等信息进行检索，同时使用Milvus来对文件标题的embedding进行向量查询以扩展搜索结果。搜索结果以rowkey与Hbase数据库关联，按这些rowkey从HBase数据库中读出文件信息。最终我们使用gradio框架搭建了一个简单的前端，用于接收用户的查询请求，并美观地展示查询结果。

系统工作流程如下面泳道图所示：
<img src="./docs/final_report/pic/system_procedure.png" width="100%" style="margin: 0 auto;">

网站已经在云服务器上部署，可以通过[USTC File Finder](http://47.76.73.185:7860/)来访问。

<img src="./docs/final_report/pic/final_website.png" width="100%" style="margin: 0 auto;">

