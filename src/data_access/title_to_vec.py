import torch
from transformers import AutoTokenizer, AutoModelForMaskedLM, BertTokenizer, BertModel
from tqdm import tqdm
import numpy as np

from config import Config

class TitleToVec:
    def __init__(self) -> None:
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = BertTokenizer.from_pretrained(
            Config.BERT_BASE_CHINESE_PATH, use_safetensors=True
        )
        self.model = BertModel.from_pretrained(
            Config.BERT_BASE_CHINESE_PATH, use_safetensors=True
        ).to(self.device)

    def generate_embedding(self, file_title):
        with torch.no_grad():
            inputs = self.tokenizer(
                file_title, truncation=True, return_tensors="pt", max_length=512
            )
            outputs = self.model(
                inputs.input_ids.to(self.device),
                inputs.token_type_ids.to(self.device),
                inputs.attention_mask.to(self.device),
            )

            # outputs.last_hidden_state.shape = torch.Size([1, 512, 768])
            # outputs.pooler_output.shape = torch.Size([1, 768])

            # tag_embedding = outputs.last_hidden_state.mean(dim=1).cpu() # 使用最后一层的平均隐藏状态作为标签的向量表示
            file_title_embedding = outputs.pooler_output.cpu()  # 使用pooler_output作为标签的向量表示
            return file_title_embedding