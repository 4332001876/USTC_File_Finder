from config import Config
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility

import numpy as np
import torch

class MilvusHelper:
    def __init__(self, collection_name):
        connections.connect(host=Config.MILVUS_HOST, port=Config.MILVUS_PORT)
        self.collection = None
        self.collection_name = collection_name
        self.create_collection()
        self.create_index()

    def get_num_entities(self):
        self.set_collection()
        self.collection.flush()
        num = self.collection.num_entities
        return num

    def set_collection(self):
        if self.has_collection():
            self.collection = Collection(name=self.collection_name)
  
    def has_collection(self):
        return utility.has_collection(self.collection_name)


    def create_collection(self):
        # Create milvus collection if not exists
        if not self.has_collection():
            file_id = FieldSchema(name="file_id",
                                    dtype=DataType.INT64,
                                    descrition="the only id for every file",
                                    is_primary=True)
                
            file_title_embedding = FieldSchema(name="file_title_embedding", 
                                            dtype=DataType.FLOAT_VECTOR, 
                                            descrition="float file_title_embedding",
                                            dim=Config.MILVUS_VECTOR_DIMENSION,
                                            is_primary=False,
                                            auto_id = False)
                
            schema = CollectionSchema(fields = [file_id, file_title_embedding], 
                                                description="file search")
                
            self.collection = Collection(name=self.collection_name, schema=schema)
        else:
            self.set_collection()
            return "OK"
        
    def create_index(self):
        # Create IVF_FLAT index on milvus collection
        self.set_collection()
        if self.collection.has_index():
            return None
        default_index = {"index_type": Config.MILVUS_INDEX_TYPE, "metric_type": Config.MILVUS_METRIC_TYPE, "params": {"nlist": 16384}}
        # * nlist:16384后续可注意是否修改
        status = self.collection.create_index(field_name="file_title_embedding", index_params=default_index, timeout=60)
        return status
        
    def search_vector(self, file_title_embedding, top_k):
        # Search vector in milvus collection
        vectors = [file_title_embedding]
        for i, vector in enumerate(vectors):
            if isinstance(vector, torch.Tensor):
                vectors[i] = vector.detach().numpy()
            if isinstance(vector, np.ndarray):
                vectors[i] = vector.astype(np.float32)
        self.set_collection()
        self.collection.load()
        search_params = {"metric_type": Config.MILVUS_METRIC_TYPE, "params": {"nprobe": 16}}
        res = self.collection.search(vectors, anns_field="file_title_embedding", param=search_params, limit=top_k)
        # res[0].ids:get the IDs of all returned hits
        # res[0].distances:get the distances to the query vector from all returned hits
        res_ids = res[0].ids
        rowkeys = [f'row_{res_id}' for res_id in res_ids]
        """if len(res[0].distances) > 0:
            print("distances:",res[0].distances[0])"""
        return rowkeys
        

    def insert_new_file(self, file_id, file_title_embedding):
        if isinstance(file_title_embedding, torch.Tensor):
            file_title_embedding = file_title_embedding.detach().numpy()
        
        self.set_collection()
        self.collection.load()
            
        if isinstance(file_title_embedding, np.ndarray):
            file_title_embedding = file_title_embedding.astype(np.float32)
            mr = self.collection.insert([[file_id, file_title_embedding]])
            id = mr.primary_keys[0]
            return id 
        else:
            raise TypeError("file_title_embedding type error, expect numpy.ndarray or torch.Tensor, got %s"%type(file_title_embedding))
