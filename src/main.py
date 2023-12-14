from data_access.search_engine import SearchEngine
from data_access.file_record import FileRecord
from server.server_backend import ServerBackend
from server.server_frontend import ServerFrontend

if __name__ == "__main__":
    search_engine = SearchEngine(init_db=False, use_milvus=False)
    server_backend = ServerBackend(search_engine)
    server_frontend = ServerFrontend(server_backend)
    server_frontend.launch()