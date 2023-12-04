import happybase
from config import Config

class FileRecord:
    def __init__(self, title, url, time, source, file_type, file_type2) -> None:
        self.title = title
        self.url = url
        self.time = time
        self.source = source
        self.file_type = file_type
        self.file_type2 = file_type2

    def __str__(self) -> str:
        return f'{self.title},{self.url},{self.time},{self.source},{self.file_type},{self.file_type2}'

    def get_hbase_data_format(self):
        return {
            b'info:title': self.title.encode(), # "string".encode() -> b"string" (bytes), 
            b'info:url': self.url.encode(),
            b'info:time': self.time.encode(),
            b'info:source': self.source.encode(),
            b'info:file_type': self.file_type.encode(),
            b'info:file_type2': self.file_type2.encode()
        }


class HbaseHelper:
    def __init__(self) -> None:
        self.connection = happybase.Connection(Config.HBASE_HOST)
        self.table = self.connection.table(Config.HBASE_TABLE_NAME)
        self.increment_id = 1

    def put_file(self, file_record: FileRecord):
        row_key = f'row_{self.increment_id}'
        row_key = row_key.encode()
        self.increment_id += 1
        self.put(row_key, file_record.get_hbase_data_format())

    def put(self, row_key, data):
        self.table.put(row_key, data)

    def get(self, row_key):
        return self.table.row(row_key)
    
    def scan(self, row_prefix):
        return self.table.scan(row_prefix=row_prefix)
    
    def delete(self, row_key):
        self.table.delete(row_key)


