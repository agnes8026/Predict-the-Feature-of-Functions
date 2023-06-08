from pathlib import Path
from tokenizers import ByteLevelBPETokenizer
from transformers import RobertaConfig
from transformers import RobertaTokenizerFast
from transformers import LineByLineTextDataset
from transformers import RobertaForMaskedLM
from transformers import DataCollatorForLanguageModeling
from transformers import Trainer, TrainingArguments
# from collections import defaultdict
# from datasets import Dataset
# import pickle

paths = [str(x) for x in Path(".").glob("**/*.txt")]
tokenizer = ByteLevelBPETokenizer()
tokenizer.train(files=paths, vocab_size=52_000, min_frequency=2, special_tokens=[
    "<s>",
    "<pad>",
    "</s>",
    "<unk>",
    "<mask>",
])
tokenizer.train(files=paths, vocab_size=52_000, min_frequency=2)

config = RobertaConfig(
    vocab_size=52_000,
    max_position_embeddings=514,
    num_attention_heads=12,
    num_hidden_layers=6,
    type_vocab_size=1,
)

## store the tokenizer for future use ##
model = RobertaForMaskedLM.from_pretrained("small-dataset-test")
# tokenizer.save_pretrained("AssemblyBERT_Roberta")
# tokenizer = RobertaTokenizerFast.from_pretrained("./AssemblyBERT_Roberta", max_len=512)


## line by line dataset ##

file_path="D:\\testproject\\dataset-mod\\combined-output.txt"

with open(file_path, "r") as file:
    text = file.read()

dataset = LineByLineTextDataset(
    tokenizer=RobertaTokenizerFast.from_pretrained("AssemblyBERT_Roberta", max_len=512),
    file_path=file_path,
    block_size=128,
)

## store the dataset for future use ##
# with open("dataset_lbl_test.pkl", "wb") as f:
#     pickle.dump(dataset, f)

## use the stored dataset ##
# with open("dataset_lbl_test.pkl", "rb") as f:
#     dataset = pickle.load(f)


## ----self defined labeled dataset(not using) start--- ##
# file_path="D:\\testproject\\dataset-mod\\combined-output.txt"
# with open(file_path, "r") as file:
#     lines = file.readlines()
# name = []
# arg_num = []
# arg_type = []
# text = []
# labeled_dataset = []
# for line in lines:
#     line = line.strip()
#     if line == "":
#         continue
#     name = line.strip().split("|")[0]
#     arg_num = int(line.strip().split("|")[1])
#     arg_type = line.strip().split("|")[2:2+arg_num]
#     text = line.strip().split("|")[2+arg_num:]
#     text.pop()
#     text_line = ' '.join(text)
#     labeled_data = (name,arg_num,arg_type,text_line)
#     labeled_dataset.append(labeled_data)

# names = []
# arg_nums = []
# arg_types = []
# texts = []
## count how many labels in a dataset 
# argnumdict = defaultdict(int)
# argtypedict = defaultdict(tuple)
# for sample in labeled_dataset:
#     names.append(sample[0])
#     arg_nums.append(sample[1])
#     arg_types.append(sample[2])
#     texts.append(sample[3])
#     argnumdict[sample[1]] += 1
#     argtypedict[tuple(sample[2])] += 1
# data = {"Name":names,"Arg_num":arg_nums,"Arg_type":arg_types,"Text":texts}
# dataset = Dataset.from_dict(data)

## ----self defined labeled dataset(not using) end--- ##

## data collator ##
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer, mlm=True, mlm_probability=0.15
)

training_args = TrainingArguments(
    output_dir="./TestBERT_Roberta",
    overwrite_output_dir=True,
    num_train_epochs=1,
    per_gpu_train_batch_size=64,
    save_steps=10_00,
    save_total_limit=2,
    prediction_loss_only=True,
)

trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=dataset,
)

trainer.train()
trainer.save_model("./TestBERT_Roberta")

## simple test set ##

# from transformers import pipeline
# fill_mask = pipeline(
#     "fill-mask",
#     model="./TestBERT_Roberta",
#     tokenizer="./TestBERT_Roberta"
# )

# print(fill_mask("strncpy <mask> char * char * typedef size_t ulong  00401e90 JMP qword ptr [0x007fe060]  "))