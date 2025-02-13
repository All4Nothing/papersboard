from transformers import pipeline, AutoTokenizer
from tqdm import tqdm
import torch
import spacy
from collections import Counter
from app.services.database import db
from app.models import Paper


device = torch.device("mps")
model = "google/flan-t5-small"

tokenizer = AutoTokenizer.from_pretrained(model)

summarizer = pipeline("summarization", model=model, device=device)
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", device=device)
extracter = spacy.load("en_core_web_sm")

candidate_labels = ["Computer Vision", "Natural Language Processing", "Reinforcement Learning", "Recommendation System"]

def classify_domain_task_with_model(title, abstract):
    text = f"{title} {abstract}"

    result = classifier(text, candidate_labels)
    return result["labels"][0]

def split_text_by_tokens(text, max_tokens=512):
    input_ids = tokenizer.encode(text, return_tensors='pt')[0]
    chunks = []
    for i in range(0, len(input_ids), max_tokens):
        chunk_ids = input_ids[i:i + max_tokens]
        chunk_text = tokenizer.decode(chunk_ids, skip_special_tokens=True)
        chunks.append(chunk_text)
    return chunks

def summarize_long_text(text, max_tokens=512):
    """
    split text into chunks and summarize each chunk
    """
    input_ids = tokenizer.encode(text, return_tensors='pt')[0]
    chunks = []

    # summarize 1st half of the text
    for i in range(0, len(input_ids), max_tokens):
        chunk_ids = input_ids[i:i + max_tokens]
        chunk_text = tokenizer.decode(chunk_ids, skip_special_tokens=True)
        chunks.append(chunk_text)

    summaries = []
    for chunk in chunks:
        max_length = min(150, len(tokenizer.encode(chunk)) // 2)
        summary = summarizer(chunk, max_length=max_length, min_length=max_length // 2, do_sample=False)
        summaries.append(summary[0]['summary_text'])
    
    # summarize all chunks
    final_summary = ' '.join(summaries)
    if len(final_summary.split()) > 100:
        final_summary = summarizer(final_summary, max_length=100, min_length=50, do_sample=False)[0]['summary_text']

    return final_summary

def summarize_paper_abstracts():
    """
    summarize abstracts of papers and update the database
    """
    papers = Paper.query.filter(Paper.abstract != None, Paper.abstract != "").all()

    for paper in tqdm(papers, desc="Summarizing papers abstracts"):
        paper.summary = summarize_long_text(paper.abstract) 
    db.session.commit()
    print("Completed summarizing papers abstracts")

def generate_weekly_report(summaries):
    combined_summaries = " ".join([summary["summary"] for summary in summaries])
    final_summary = summarize_long_text(combined_summaries)
    # 보기 좋게 문단으로 나누기 (마침표를 기준으로)
    sentences = final_summary.split(". ")
    formatted_summary = "\n\n".join(". ".join(sentences[i:i+3]) for i in range(0, len(sentences), 3))
    
    # 보고서 작성
    report = f"이번 주 인공지능 분야의 주요 논문 요약 보고서:\n\n{formatted_summary}"
    return report

def extract_keywords(text, top_n=5):
    """
    extract keywords from abstract of papers
    """
    doc = extracter(text.lower())
    keywords = [token.text for token in doc if token.is_alpha and not token.is_stop]
    most_common_keywords = [word for word, _ in Counter(keywords).most_common(top_n)]

    return most_common_keywords