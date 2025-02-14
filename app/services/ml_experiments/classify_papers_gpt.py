import openai
import csv
import difflib
from app.models import Paper
from app import create_app, db

app = create_app()

GPT_MODEL = "gpt-4o"

ML_SUBFIELDS = [
    "Natural Language Processing", 
    "Computer Vision",
    "Reinforcement Learning",
    "Recommendation System"
    "Generative Models",
    "Time Series Analysis",
    "Anomaly Detection",
    "Robotics",
]

def classify_with_gpt(title, abstract, url):
    prompt = f"""
    You are an expert in Machine Learning Research.

    Given the title and abstract of a research paper, classify the paper into one of the following subfields of machine learning:
    **Subfields:** {", ".join(ML_SUBFIELDS)}

    **Title:** {title}
    **Abstract:** {abstract}
    **Link:** {url}

    If the paper does not fit any of the existing subfields, suggest a new subfield.
    Respond in the format: "Existing Field: [field_name]" or "New Field: [new_field_name]".
    """

    client = openai.OpenAI()

    response = client.chat.completions.create(
        model = GPT_MODEL,
        messages = [{"role": "system", "content": "You are an AI trained to classify machine learning papers."},
                    {"role": "user", "content": prompt}],
        temperature = 0.2
    )

    return response["choices"][0]["message"]["content"].strip()

def find_best_match(field, existing_fields, threshold=0.7):
    best_match = difflib.get_close_matches(field, existing_fields, n=1, cutoff=threshold)
    return best_match[0] if best_match else None

def classify_papers_with_gpt():
    with app.app_context():
        papers = Paper.query.all()
        new_fields = set()

        with open("ground_truth_dataset.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Title", "Abstract", "URL", "GPT_Label"])

            for paper in papers:
                gpt_label = classify_with_gpt(paper.title, paper.abstract, paper.url)

                if gpt_label.startswith("New Field:"):
                    new_field = gpt_label.split(":")[1].strip()
                    best_match = find_best_match(new_field, ML_SUBFIELDS)
                    
                    if best_match:
                        print(f"New field '{new_field}' matches existing field '{best_match}'")
                        gpt_label = best_match
                    else:
                        print(f"New field detected: {new_field}")
                        new_fields.add(new_field)
                        gpt_label = new_field
                elif gpt_label.startswith("Existing Field:"):
                    gpt_label = gpt_label.replace("Existing Field:", "").strip()

                writer.writerow([paper.title, paper.abstract, paper.url, gpt_label])
                print(f"✅ Classified: {paper.title} -> {gpt_label}")

        if new_fields:
            with open("new_fields.log", "w") as log_file:
                log_file.write("\n".join(new_fields))
            print("New fields logged in 'new_fields.log'")
        
        print("✅ Ground truth dataset created")

if __name__ == "__main__":
    classify_papers_with_gpt()