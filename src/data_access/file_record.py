class FileRecord:
    def __init__(self, title, url, time, source, file_type, file_type_2) -> None:
        self.title = str(title)
        self.url = str(url)
        self.time = str(time)
        self.source = str(source)
        self.file_type = str(file_type)
        self.file_type_2 = str(file_type_2)

    def __str__(self) -> str:
        return f'{self.title},{self.url},{self.time},{self.source},{self.file_type},{self.file_type2}'

    def get_hbase_data_format(self):
        return {
            b'info:title': self.title.encode(), # "string".encode() -> b"string" (bytes), 
            b'info:url': self.url.encode(),
            b'info:time': self.time.encode(),
            b'info:source': self.source.encode(),
            b'info:file_type': self.file_type.encode(),
            b'info:file_type_2': self.file_type_2.encode()
        }