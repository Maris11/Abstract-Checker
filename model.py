import gc
import pandas as pd
import torch
from torch import nn
from torch.utils.data import TensorDataset, DataLoader
from transformers import AutoTokenizer, AutoModel


class IsGenerated(nn.Module):
    def __init__(self, embedding_dim, hidden_dim):
        super(IsGenerated, self).__init__()
        self.fc1 = nn.Linear(embedding_dim, hidden_dim)
        self.dropout = nn.Dropout(p=0.2)
        self.fc2 = nn.Linear(hidden_dim, 1)
        self.sigmoid = nn.Sigmoid()

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
        text_sequence_size: int = 30,
        shuffle: bool = True,
        language: str = "latvian",
        device: str = torch.device('cuda'),
        load_model: bool = True,
        model_path: str = "model_latvian.pt",
        seed: int = 42
):
    if seed:
        torch.manual_seed(seed)

    bert_model_name = "AiLab-IMCS-UL/lvbert" if language == "latvian" else "bert-base-uncased"

    # Load pre-trained BERT tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(bert_model_name)
    model = AutoModel.from_pretrained(bert_model_name).to(device)

    # Preprocess input sentences
    sentence_text = list(sentences.sentence)

    # Tokenize sentences and convert to input IDs
    input_ids = []
    for sentence in sentence_text:
        encoded_dict = tokenizer.encode_plus(
            sentence,
            add_special_tokens=True,
            max_length=text_sequence_size,
            truncation=True,
            padding='max_length',
            return_tensors='pt'
        )
        input_ids.append(encoded_dict['input_ids'])

    ids = torch.cat(input_ids, dim=0).to(device)
    del input_ids

    gc.collect()
    torch.cuda.empty_cache()
    # Compute sentence embeddings using BERT model
    with torch.no_grad():
        outputs = model(ids)
        embeddings = outputs[0][:, 0, :]

    # Create dataset and data loader
    if with_is_generated:
        generated = torch.tensor(sentences.is_generated.values, dtype=torch.float).to(device)
        dataset = TensorDataset(embeddings, generated)
    else:
        dataset = TensorDataset(embeddings)

    data_loader = DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)
    model = IsGenerated(768, text_sequence_size).to(device)

    if load_model and model_path:
        model.load_state_dict(torch.load(model_path))
        model = model.to(device)

    return data_loader, model
