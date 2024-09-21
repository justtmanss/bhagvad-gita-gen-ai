import json
import torch
from sklearn.model_selection import train_test_split
from transformers import GPT2LMHeadModel, GPT2Tokenizer, Trainer, TrainingArguments

# Load chapters
with open('/Users/aakashvenkatraman/Documents/GitHub/bahgvad-gita-gen-ai/backend/database/data/genai.chapter.json', 'r', encoding='utf-8') as chapter_file:
    chapters = json.load(chapter_file)

# Load slokas
with open('/Users/aakashvenkatraman/Documents/GitHub/bahgvad-gita-gen-ai/backend/database/data/genai.sloka.json', 'r', encoding='utf-8') as sloka_file:
    slokas = json.load(sloka_file)

# Combine chapters and slokas into a single dataset for training
data = []
for chapter in chapters:
    for sloka in slokas:
        if sloka['chapterNumber'] == chapter['chapterNumber']:
            data.append({
                'question': f"What does Chapter {chapter['chapterNumber']} say?",
                'answer': sloka['sloka']
            })

# Split data into training and validation sets
train_data, val_data = train_test_split(data, test_size=0.2, random_state=42)

# Load tokenizer and model
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

# Set padding token
tokenizer.pad_token = tokenizer.eos_token  # or use a new token: tokenizer.add_special_tokens({'pad_token': '[PAD]'})

# Tokenize the data
def tokenize_data(data):
    return tokenizer(data['question'], return_tensors='pt', padding=True, truncation=True)

train_encodings = [tokenize_data(d) for d in train_data]
val_encodings = [tokenize_data(d) for d in val_data]

# Prepare dataset class
class CustomDataset(torch.utils.data.Dataset):
    def __init__(self, encodings):
        self.encodings = encodings

    def __getitem__(self, idx):
        return {key: val[idx] for key, val in self.encodings[idx].items()}

    def __len__(self):
        return len(self.encodings)

train_dataset = CustomDataset(train_encodings)
val_dataset = CustomDataset(val_encodings)

# Training arguments
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
)

# Train the model
trainer.train()

# Function to answer user queries
def answer_query(query):
    inputs = tokenizer.encode(query, return_tensors='pt')
    outputs = model.generate(inputs, max_length=50)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

# Example usage
user_query = "What does Chapter 1 say?"
response = answer_query(user_query)
print(response)
