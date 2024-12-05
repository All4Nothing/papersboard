from transformers import pipeline, AutoTokenizer
from tqdm import tqdm
import torch
device = 0 if torch.cuda.is_available() else -1

tokenizer = AutoTokenizer.from_pretrained("t5-small")

summarizer = pipeline("summarization", model="t5-small", device=device)

def split_text_by_tokens(text, max_tokens=512):
    input_ids = tokenizer.encode(text, return_tensors='pt')[0]
    chunks = []
    for i in range(0, len(input_ids), max_tokens):
        chunk_ids = input_ids[i:i + max_tokens]
        chunk_text = tokenizer.decode(chunk_ids, skip_special_tokens=True)
        chunks.append(chunk_text)
    return chunks

def summarize_long_text(text, max_tokens=512):
    chunks = split_text_by_tokens(text, max_tokens)
    summaries = []
    for chunk in chunks:
        input_length = len(tokenizer.encode(chunk))
        max_length = min(150, input_length // 2)
        summary = summarizer(chunk, max_length=max_length, min_length=max_length // 2, do_sample=False)
        summaries.append(summary[0]['summary_text'])
    final_summary = ' '.join(summaries)
    return final_summary

def summarize_paper_abstracts(papers):
    """
    논문 초록을 요약합니다.
    """
    summaries = []
    for paper in tqdm(papers, desc="Summarizing papers"):
        abstract = paper["abstract"]
        # 입력 텍스트의 단어 수를 계산
        input_length = len(abstract.split())
        # max_length를 입력 길이에 맞게 조정
        max_length = min(150, input_length)
        # 요약 생성
        # summary = summarizer(abstract, max_length=max_length, min_length=max_length // 2, do_sample=False)
        summary = summarize_long_text(abstract)
        summaries.append({"title": paper["title"], "summary": summary})
    return summaries

def generate_weekly_report(summaries):
    combined_summaries = " ".join([summary["summary"] for summary in summaries])
    final_summary = summarize_long_text(combined_summaries)
    # 보기 좋게 문단으로 나누기 (마침표를 기준으로)
    sentences = final_summary.split(". ")
    formatted_summary = "\n\n".join(". ".join(sentences[i:i+3]) for i in range(0, len(sentences), 3))
    
    # 보고서 작성
    report = f"이번 주 인공지능 분야의 주요 논문 요약 보고서:\n\n{formatted_summary}"
    return report