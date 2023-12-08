from elasticsearch import Elasticsearch

from config import Config
from data_access.file_record import FileRecord

class ElasticsearchHelper:
    def __init__(self) -> None:  
        # connect
        self.es = Elasticsearch(host="0.0.0.0",port=9200,timeout=60)

    def insert(self, rowkey, file_record: FileRecord):
        # insert
        data = {
            "rowkey":rowkey,
            "title":file_record.title
        }
        self.es.index(index=Config.ELASTIC_SEARCH_INDEX_NAME,body=data)

    def query(self, keyword):
        # query
        query = {
            "query":{
                "term":{
                    "title":keyword
                }
            }
        }
        results = self.es.search(index=Config.ELASTIC_SEARCH_INDEX_NAME,body=query)
        rowkeys = [result['_source']["rowkey"] for result in results['hits']['hits']]
        return rowkeys
    
    def rowkey_to_id(self, rowkey):
        query = {
            "query":{
                "term":{
                    "rowkey":rowkey
                }
            }
        }
        results = self.es.search(index=Config.ELASTIC_SEARCH_INDEX_NAME,body=query)
        ids = [result['_id'] for result in results['hits']['hits']]
        return ids

    def delete(self, rowkey):
        ids = self.rowkey_to_id(rowkey)
        for id in ids:
            # delete
            self.es.delete(index=Config.ELASTIC_SEARCH_INDEX_NAME,id=id)

    def update(self, rowkey, file_record: FileRecord):
        ids = self.rowkey_to_id(rowkey)
        for id in ids:
            # update
            data = {
                "rowkey":rowkey,
                "title":file_record.title
            }
            self.es.update(index=Config.ELASTIC_SEARCH_INDEX_NAME,id=id,body=data)