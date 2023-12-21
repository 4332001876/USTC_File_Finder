from server.server_backend import ServerBackend

from config import Config

import gradio as gr
import pandas as pd

import os


class ServerFrontend:
    def __init__(self, server_backend:ServerBackend) -> None:
        self.server_backend = server_backend
        self.page = self.build_page()

    def build_page(self):
        
        with gr.Blocks() as page:
            
            gr.Markdown("# USTC File Finder")
            gr.Markdown("use the search engine to find the file you want")   

            input_keyword = gr.Textbox("keyword")
            image_button = gr.Button("Query",scale=1)
            
            gr.Markdown("## Result")
            gr.Markdown("Click on the title to access the file.")   
            
            # ui_content=[]
            table_output = gr.DataFrame(
                headers=["title", "time", "source"],
                datatype=["markdown", "str", "str"],
                row_count=(5, 'dynamic'),
                col_count=(3, "fixed")
            )
            # ui_content.append(table_output)

            image_button.click(fn=self.server_backend.get_query_result_ui, inputs=input_keyword, outputs=table_output, api_name="greet")

        return page

    def launch(self):
        self.page.launch(server_name="0.0.0.0")

    
    
