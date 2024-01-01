import pandas as pd

from config import Config
from data_access.file_record import FileRecord
from data_access.hbase_helper import HbaseHelper
from data_access.elastic_search_helper import ElasticsearchHelper
from data_access.milvus_helper import MilvusHelper
from data_access.title_to_vec import TitleToVec

'''
hbase字段
- b'info:title'
- b'info:url'
- b'info:time'
- b'info:source'
- b'info:file_type'
- b'info:file_type_2'
'''

class SearchEngine:
    def __init__(self, init_db = False, use_milvus = False) -> None:
        self.hbase = HbaseHelper()
        self.es = ElasticsearchHelper()
        self.use_milvus = use_milvus
        if use_milvus:
            self.milvus = MilvusHelper(Config.MILVUS_DB_NAME)
            self.title_to_vec = TitleToVec()
        if init_db:
            self.init_db()
    
    def insert(self, file_record: FileRecord):
        file_id, row_key = self.hbase.put_file(file_record)
        self.es.insert(row_key, file_record)
        if self.use_milvus:
            file_title_embedding = self.title_to_vec.generate_embedding(file_record.title)
            self.milvus.insert_new_file(file_id, file_title_embedding)

    def init_db(self):
        data = pd.read_csv(Config.FILE_LIST_PATH)
        for i in range(data.shape[0]):
            file_record = FileRecord(
                title=data["title"][i],
                url=data["url"][i],
                time=data["time"][i],
                source=data["source"][i],
                file_type=data["file_type"][i],
                file_type_2=data["file_type_2"][i]
            )     
            self.insert(file_record)
    
    def query(self, keyword, source=None):
        # 先从es中搜索
        rowkeys = self.es.query(keyword, source)
        if len(rowkeys)>Config.TOP_K:
            rowkeys = rowkeys[:Config.TOP_K]

        # 若开启了向量查询，再从milvus中搜索
        if self.use_milvus:
            title_embedding = self.title_to_vec.generate_embedding(keyword)
            milvus_rowkeys = self.milvus.search_vector(title_embedding, Config.MILVUS_TOP_K)
            rowkeys = self.merge_search_result_simple(rowkeys, milvus_rowkeys) # 合并搜索结果，并保证搜索结果的排序

        # 以rowkey从hbase中获取文件信息
        file_records = []
        for rowkey in rowkeys:
            file_record = self.hbase.get_file(rowkey)
            # 校验文件来源网站
            if (source is not None) and source != Config.SOURCE_ALL:
                if file_record.source != source:
                    continue
            file_records.append(file_record)
        return file_records

    def merge_search_result_simple(self, es_rowkeys, milvus_rowkeys):
        rowkeys = es_rowkeys
        es_rowkeys_set = set(es_rowkeys)
        for rowkey in milvus_rowkeys:
            if rowkey not in es_rowkeys_set:
                rowkeys.append(rowkey)

        if len(rowkeys)>Config.TOP_K:
            rowkeys = rowkeys[:Config.TOP_K]      
        return rowkeys

    def merge_search_result(self, es_rowkeys, milvus_rowkeys):
        rowkeys = []
        es_rowkeys_set = set(es_rowkeys)
        milvus_rowkeys_not_in_es = []
        # 先把两个搜索结果交集存入集合
        for rowkey in milvus_rowkeys:
            if rowkey in es_rowkeys_set:
                rowkeys.append(rowkey)
                es_rowkeys_set.remove(rowkey)
            else:
                milvus_rowkeys_not_in_es.append(rowkey)

        # 交错合并剩余结果
        milvus_rowkeys_not_in_es = milvus_rowkeys_not_in_es[::-1] # 反转列表，使得优先级最高的在最后面，便于pop操作
        for rowkey in es_rowkeys_set:
            rowkeys.append(rowkey)
            if len(milvus_rowkeys_not_in_es) > 0:
                rowkeys.append(milvus_rowkeys_not_in_es.pop())
        rowkeys += milvus_rowkeys_not_in_es

        if len(rowkeys)>Config.TOP_K:
            rowkeys = rowkeys[:Config.TOP_K]      
        return rowkeys





