class Config:
    # crawler
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.46"
    COOKIE = r"s_fid=64116D8E61735942-31EC6D99BABB0880;"
    SLEEP_TIME = 0.2 # second
    
    # path
    TMP_PATH = "tmp"
    FILE_LIST_PATH = "./crawler/file_list.csv"

    # search engine
    TOP_K = 100

    # hbase
    HBASE_HOST = "0.0.0.0"
    HBASE_PORT = 9090
    HBASE_TABLE_NAME = "ustc_file_finder_v3"

    # milvus
    MILVUS_HOST = "0.0.0.0"
    MILVUS_PORT = 19530
    MILVUS_VECTOR_DIMENSION = 768
    MILVUS_DB_NAME = "ustc_file_finder"
    MILVUS_METRIC_TYPE = "COSINE"
    MILVUS_TOP_K = 50
    MILVUS_INDEX_TYPE = "IVF_FLAT"
    BERT_BASE_CHINESE_PATH = "/home/admin/bert-base-chinese"

    # elastic search
    ELASTIC_SEARCH_INDEX_NAME = "ustc_file_finder_v3"

    # front-end
    SOURCE_CHOICES = ['教务处', '研究生院', '软件学院', '先进技术研究院', '网络信息中心', '国际合作与交流部', '超算中心', '学工在线', '信息科学技术学院', '出版社', 
        '苏州高等研究院', '资产与后勤保障处', '计算机科学技术学院', '保卫与校园管理处', '信息科学实验中心', '科技成果转移转化办公室', '网络空间安全学院', '大数据学院', '工程科学学院']
    SOURCE_ALL = "All"