import time
import sqlite3
import pandas as pd
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from tqdm import tqdm
from app.services.ml_experiments.data_preprocess import preprocess_abstract_data

device = torch.device("mps")

models = [
    # "google/flan-t5-base",
    # "google/flan-t5-large",
    # "google/flan-t5-xl"
    # "facebook/bart-large-cnn",
    "sshleifer/distilbart-cnn-6-6"
]

db_path = "papers.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

df = pd.read_sql_query("SELECT id, title, abstract FROM papers LIMIT 100", conn)

results = {}




for model_name in models:
    print(f"🚀 Loading model {model_name}")

    model = AutoModelForSeq2SeqLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
        device_map="auto"
    )

    tokenizer = AutoTokenizer.from_pretrained(model_name)

    summarizer = pipeline("summarization", model=model_name, tokenizer=tokenizer, device=device)

    total_time = 0
    summaries = []

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    

    for idx, row in tqdm(df.iterrows(), total=len(df), desc=f"Summarizing with {model_name}", unit="paper"):
        start_time = time.time()
        preprocessed_data = preprocess_abstract_data(row["abstract"])
        summary = summarizer(preprocessed_data, max_length=150, min_length=50, do_sample=False)[0]['summary_text']

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