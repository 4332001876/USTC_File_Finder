import pandas as pd

from data_access.search_engine import SearchEngine
from data_access.file_record import FileRecord

class ServerBackend:
    def __init__(self, search_engine:SearchEngine) -> None:
        self.search_engine = search_engine

    def get_query_result_ui(self, keyword, source=None):
        file_records = self.search_engine.query(keyword, source)
        df= pd.DataFrame(columns=["title","time","source"])
        for file_record in file_records:
            link_element_code = "[%s](%s)"%(file_record.title, file_record.url)
            # link_element_code = "<a href=\"%s\">%s<\\a>"%(file_record.url, file_record.title)
            df.loc[len(df)] = [link_element_code, file_record.time, file_record.source]

        # Function to apply text color
        def highlight_cols(x): 
            df = x.copy() 
            df.loc[:, :] = 'color: black'
            df["title"] = 'color: #2440b3; font-weight: 500;'
            return df 
        # Applying the style function
        df = df.style.apply(highlight_cols, axis = None)

        # print(df.describe())
        # print(df.head())
        ui_content = df
        return ui_content

