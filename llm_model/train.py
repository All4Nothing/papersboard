import numpy as np 
import pandas as pd 
import torch

from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, BitsAndBytesConfig, DataCollatorForSeq2Seq, Seq2SeqTrainer, Seq2SeqTrainingArguments
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training, TaskType

def preprocess_data(df):
    inputs = [data for data in df['article']]

    model_inputs = tokenizer(inputs, max_length=512, truncation=True, padding="max_length")

    with tokenizer.as_target_tokenizer():
        labels = tokenizer(df['highlights'], max_length=128, truncation=True, padding="max_length")

    model_inputs["labels"] = labels["input_ids"]

    return model_inputs


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
dataset = load_dataset("cnn_dailymail", "3.0.0")

model_name = "google/flan-t5-base"

tokenizer = AutoTokenizer.from_pretrained(model_name)

encoded_dataset = dataset.map(preprocess_data, batched=True)
train_dataset = encoded_dataset["train"].shuffle(seed=42).select(range(12000))
test_dataset = encoded_dataset["validation"].shuffle(seed=42).select(range(5600))

bnb_config = BitsAndBytesConfig(
    load_in_8bit = True,
)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name, quantization_config=bnb_config, device_map="auto")

lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q", "v"],
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.SEQ_2_SEQ_LM
)

model = prepare_model_for_kbit_training(model)
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

label_pad_token_id = -100

data_collator = DataCollatorForSeq2Seq(
    tokenizer,
    model=model,
    label_pad_token_id=label_pad_token_id,
    pad_to_multiple_of=8
)

output_dir = "lora-flan-t5-base"

training_args = Seq2SeqTrainingArguments(
    output_dir = output_dir,
    auto_find_batch_size = True,
    learning_rate=1e-3,
    num_train_epochs=5,
    logging_dir=f"{output_dir}/logs",
    logging_strategy="steps",
    logging_steps=500,
    save_strategy="no",
    report_to="tensorboard",
)

trainer = Seq2SeqTrainer(
    model = model,
    args = training_args,
    data_collator=data_collator,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
)

model.config.use_cache = False

trainer.train()
peft_model_name="results"
trainer.model.save_pretrained(peft_model_name)
tokenizer.save_pretrained(peft_model_name)

trainer.evaluate()