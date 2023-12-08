from data_access.search_engine import SearchEngine
from data_access.file_record import FileRecord
from server.server_backend import ServerBackend
from server.server_frontend import ServerFrontend

class Tester:
    def __init__(self) -> None:
        pass

    def test_whole_system(self, init_db = False):
        search_engine = SearchEngine(init_db=init_db, use_milvus=True)
        server_backend = ServerBackend(search_engine)
        server_frontend = ServerFrontend(server_backend)
        server_frontend.launch()

if __name__ == "__main__":
    tester = Tester()
    tester.test_whole_system(init_db = False)