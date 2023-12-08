import happybase
from config import Config

from data_access.file_record import FileRecord

class HbaseHelper:
    def __init__(self) -> None:
        self.connection = happybase.Connection(host=Config.HBASE_HOST,port=Config.HBASE_PORT, autoconnect=True)
        if Config.HBASE_TABLE_NAME not in [name.decode() for name in self.connection.tables()]:
            self.connection.create_table(
                Config.HBASE_TABLE_NAME,
                {
                    'info': dict(),  # use defaults
                    'counter': dict()
                }
            )
        self.table = self.connection.table(Config.HBASE_TABLE_NAME)

    def put_file(self, file_record: FileRecord):
        increment_id = self.table.counter_inc(b'row_increment_id', b'counter:increment_id')
        row_key_str = f'row_{increment_id}'
        row_key = row_key_str.encode()
        self.put(row_key, file_record.get_hbase_data_format())
        return increment_id, row_key_str

    def get_file(self, row_key):
        row = self.get(row_key)
        if row:
            return FileRecord(
                tilte = row[b'info:title'].decode(),
                url = row[b'info:url'].decode(),
                time = row[b'info:time'].decode(),
                source = row[b'info:source'].decode(),
                file_type = row[b'info:file_type'].decode(),
                file_type_2 = row[b'info:file_type_2'].decode()
            )
        else:
            return None


    def put(self, row_key, data):
        self.table.put(row_key, data)

    def get(self, row_key):
        return self.table.row(row_key)
    
    def scan(self, row_prefix):
        return self.table.scan(row_prefix=row_prefix)
    
    def delete(self, row_key):
        self.table.delete(row_key)


