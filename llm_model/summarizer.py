from tqdm import tqdm
import torch
from collections import Counter
from app.services.database import db
from app.models import Paper
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM, BitsAndBytesConfig
from peft import PeftModel, PeftConfig


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model_name = "google/flan-t5-base"

peft_model_name = "../papersboard/ml_model/results"
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