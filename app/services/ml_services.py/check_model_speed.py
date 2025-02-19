import time
import sqlite3
import pandas as pd
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from tqdm import tqdm
from peft import get_peft_model, LoraConfig, TaskType

from app.services.ml_experiments.data_preprocess import preprocess_abstract_data

device = torch.device("mps")

models = [
    "google/flan-t5-base",
]

db_path = "papers.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

df = pd.read_sql_query("SELECT id, title, abstract FROM papers LIMIT 100", conn)

results = {}




for model_name in models:
    print(f"🚀 Loading model {model_name}")

    lora_config = LoraConfig(
        task_type=TaskType.SEQ_2_SEQ_LM,
        r=8,
        lora_alpha=32,
        lora_dropout=0.1
    )

    model = AutoModelForSeq2SeqLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
    )


    model = get_peft_model(model, lora_config)
    model.to(device)  # 모델을 GPU/MPS로 이동

    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # summarizer = pipeline("summarization", model=model, tokenizer=tokenizer, device=device)

    total_time = 0
    summaries = []
    

    for idx, row in tqdm(df.iterrows(), total=len(df), desc=f"Summarizing with {model_name}", unit="paper"):
        start_time = time.time()
        preprocessed_data = preprocess_abstract_data(row["abstract"])

        inputs = tokenizer(preprocessed_data, return_tensors="pt", max_length=512, truncation=True).to(device)
        outputs = model.generate(**inputs, max_length=150, min_length=50)
        summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
        # summary = summarizer(preprocessed_data, max_length=150, min_length=50, do_sample=False)[0]['summary_text']

        elapsed_time = time.time() - start_time
        total_time += elapsed_time
        summaries.append((row['id'], summary))

    avg_time_per_paper = total_time / len(df)
    print(f"🕒 Average time per paper: {avg_time_per_paper:.2f} seconds")

    results[model_name] = {
        "avg_summary_time": avg_time_per_paper,
    }

conn.close()

print("📊 Summary Time Results")
for model, times in results.items():
    print(f"{model}: {times['avg_summary_time']:.2f} seconds")