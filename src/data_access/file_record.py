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