import pandas as pd
import torch

from Module import create_data_loader_and_model

device = torch.device('cuda')
torch.manual_seed(42)

sentences = pd.read_csv(
    "test_data.csv",
    delimiter=',',
    encoding='utf-8',
    header=0
)

with open("model.bin", "r") as f:
    seq_size = int(f.read())

data_loader, model = create_data_loader_and_model(sentences, text_sequence_size=seq_size, embedding_dim=200)
model.load_state_dict(torch.load("model.tar"))
model = model.to(device)

correct_generated = 0
correct_real = 0
generated_count = 0
real_count = 0

for text, generated in data_loader:
    out = model(text)
    is_correct = torch.round(out[0]) == generated[0]

    if generated[0] == 1:
        generated_count = generated_count + 1
    else:
        real_count = real_count + 1

    if is_correct:
        if generated[0] == 1:
            correct_generated = correct_generated + 1
        else:
            correct_real = correct_real + 1

print(correct_generated, correct_real, generated_count, real_count)

print("Generated Precision: {:.1f}%\nReal Precision: {:.1f}%\nOverall precision: {:.1f}%".format(
    correct_generated / generated_count * 100,
    correct_real / real_count * 100,
    (correct_real + correct_generated) / len(data_loader) * 100
))
