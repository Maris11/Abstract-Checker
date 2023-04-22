import gc
import pandas as pd
import torch
from torch import nn
from torch.utils.data import TensorDataset, DataLoader
from transformers import AutoTokenizer, AutoModel

device = torch.device('cuda')
torch.manual_seed(42)


class IsGenerated(nn.Module):
    def __init__(self, embedding_dim, hidden_dim):
        super(IsGenerated, self).__init__()
        self.fc1 = nn.Linear(embedding_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, 1)
        self.sigmoid = nn.Sigmoid()
        self.dropout = nn.Dropout(p=0.2)

    def forward(self, x):
        out = self.fc1(x)
        out = self.dropout(out)
        out = self.fc2(out)
        out = self.sigmoid(out)
        return out.squeeze()


def create_data_loader_and_model(
        sentences: pd.DataFrame,
        batch_size: int = 1,
        with_is_generated: bool = True,
        text_sequence_size: int = 25,
        shuffle: bool = True,
        bert_model_name: str = "AiLab-IMCS-UL/lvbert"
):
    # Load pre-trained BERT tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(bert_model_name)
    model = AutoModel.from_pretrained(bert_model_name).to(device)

    # Preprocess input sentences
    sentence_text = list(sentences.sentence)

    # Tokenize sentences and convert to input IDs
    input_ids = []
    attention_masks = []
    for sentence in sentence_text:
        encoded_dict = tokenizer.encode_plus(
            sentence,
            add_special_tokens=True,
            max_length=text_sequence_size,
            truncation=True,
            padding='max_length',
            return_attention_mask=True,
            return_tensors='pt'
        )

        input_ids.append(encoded_dict['input_ids'])
        attention_masks.append(encoded_dict['attention_mask'])

    # Convert input IDs and attention masks to tensors and move to device
    input_ids = torch.cat(input_ids, dim=0).to(device)
    attention_masks = torch.cat(attention_masks, dim=0).to(device)

    gc.collect()
    torch.cuda.empty_cache()
    # Compute sentence embeddings using BERT model
    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_masks)
        embeddings = outputs[0][:, 0, :]

    # Create dataset and data loader
    if with_is_generated:
        generated = torch.tensor(sentences.is_generated.values, dtype=torch.float).to(device)
        dataset = TensorDataset(embeddings, generated)
    else:
        dataset = TensorDataset(embeddings)

    data_loader = DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)
    model = IsGenerated(768, text_sequence_size).to(device)

    return data_loader, model
