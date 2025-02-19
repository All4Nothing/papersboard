from tqdm import tqdm
import torch
from collections import Counter
from app.services.database import db
from app.models import Paper
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM, BitsAndBytesConfig
from peft import PeftModel, PeftConfig


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model_name = "google/flan-t5-base"

peft_model_name = "../papersboard/app/services/ml_services/results"
config = PeftConfig.from_pretrained(peft_model_name)

bnb_config = BitsAndBytesConfig(
    load_in_8bit = True,
)

model = AutoModelForSeq2SeqLM.from_pretrained(config.base_model_name_or_path, quantization_config=bnb_config, device_map={"":0})
tokenizer = AutoTokenizer.from_pretrained(config.base_model_name_or_path)

model = PeftModel.from_pretrained(model, peft_model_name, device_map={"":0})
model.eval()

def summarize_abstract(text, max_tokens=512):
    input_ids = tokenizer(text, return_tensors="pt", truncation=True).input_ids.cuda()
    outputs = model.generate(input_ids=input_ids, max_new_tokens=150, do_sample=True, top_p=0.9)
    summary = tokenizer.batch_decode(outputs.detach().cpu().numpy(), skip_special_tokens=True)[0]
    
    return summary

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