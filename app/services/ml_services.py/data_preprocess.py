import re

def preprocess_abstract_data(text):
    # Remove line breaks (\n) and normalize whitespace
    text = re.sub(r'\s+', ' ', text.replace("\n", " ")).strip()
    # Eliminate unnecessary special characters (except: parentheses)
    text = re.sub(r'[^a-zA-Z0-9()\s+\-*/=%<>^|&~.]|(?<!\d)\.(?!\d)', '', text)
    # Convert multiple consecutive spaces into a single space
    text = re.sub(r'\s+', ' ', text)

    return text