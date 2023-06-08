from transformers import RobertaTokenizerFast
from transformers import RobertaForMaskedLM
from transformers import Trainer, TrainingArguments
import pickle

## load tokeizer and model ##
tokenizer = RobertaTokenizerFast.from_pretrained('AssemblyBERT_Roberta')
model = RobertaForMaskedLM.from_pretrained("small-dataset-test")

## load dataset ##
with open("dataset_lbl_test.pkl", "rb") as f:
    dataset = pickle.load(f)

## encoding dataset ##
def tokenize_function(example):
    return tokenizer(example["text"], truncation=True, padding='max_length')

tokenized_dataset = dataset.map(tokenize_function, batched=True)

training_args = TrainingArguments(
    output_dir='finetunetest', 
    learning_rate=1e-4,
    num_train_epochs=3,
    per_device_train_batch_size=8, 
    save_total_limit=1,
    save_strategy='epoch' 
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
)

trainer.train()
