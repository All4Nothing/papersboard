from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, BitsAndBytesConfig
from peft import PeftModel, PeftConfig
import torch


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

sample = "Jarryd Hayne's move to the NFL is a boost for rugby league in the United States, it has been claimed. The Australia international full-back or centre quit the National Rugby League in October to try his luck in American football and was this week given a three-year contract with the San Francisco 49ers. Peter Illfield, chairman of US Association of Rugby League, said: 'Jarryd, at 27, is one of the most gifted and talented rugby league players in Australia. He is an extraordinary athlete. Jarryd Hayne (right) has signed with the San Francisco 49ers after quitting the NRL in October . Hayne, who played rugby league for Australia, has signed a three year contract with the 49ers . 'His three-year deal with the 49ers, as an expected running back, gives the USA Rugby League a connection with the American football lover like never before. 'Jarryd's profile and playing ability will bring our sport to the attention of many. It also has the possibility of showing the American college athlete the possibilities of transition and adaptation for them to play rugby league, should they desire. 'Part of our recruitment strategy is aimed at the American football player who has excelled at High School level but just misses out on their College football team in their Freshman year. Hayne could play at full back or centre in rugby league and is expected to be a running back for the 49ers . 'There is no community football for that high-level of athlete. Rugby league is the perfect sport for him and we now have Jarryd as a first-hand role model.' Illfield has invited Hayne to be a guest of honour at the USARL fixtures in their 14-club competition over the summer, adding: 'We are looking at every source for increasing performance outcomes for the USA national team leading up to the 2017 Rugby League World Cup in Australia and New Zealand.'"

input_ids = tokenizer(sample, return_tensors="pt", truncation=True).input_ids.cuda()
outputs = model.generate(input_ids=input_ids, max_new_tokens=150, do_sample=True, top_p=0.9)
print(f"input sentence: {sample}\n{'---'*20}")

print(f"highlights:\n{tokenizer.batch_decode(outputs.detach().cpu().numpy(), skip_special_tokens=True)[0]}")

