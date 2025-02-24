def process_paper_data(raw_data):
    processed_data = []
    for entry in raw_data:
        processed_data.append({
            "title": entry.get("title", ""),
            "abstract": entry.get("summary", ""),
            "authors": ", ".join(entry.get("author", [])),
            "submitted_date": entry.get("submittedDate", ""),
        })
    return processed_data