import pandas as pd

from data_access.search_engine import SearchEngine
from data_access.file_record import FileRecord

class ServerBackend:
    def __init__(self, search_engine:SearchEngine) -> None:
        self.search_engine = search_engine

    def get_query_result_ui(self, keyword):
        file_records = self.search_engine.query(keyword)
        df= pd.DataFrame(columns=["title","url","time","source"])
        for file_record in file_records:
            df.loc[len(df)] = [file_record.title, file_record.url, file_record.time, file_record.source]
        ui_content = [df]
        return ui_content

