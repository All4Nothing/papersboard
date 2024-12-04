def process_paper_data(raw_data):
    # 예: arXiv에서 가져온 데이터를 파싱하고 필요한 필드만 추출
    processed_data = []
    for entry in raw_data:  # raw_data는 arXiv API에서 가져온 데이터 구조
        processed_data.append({
            "title": entry.get("title", ""),
            "abstract": entry.get("summary", ""),
            "authors": ", ".join(entry.get("author", [])),
            "submitted_date": entry.get("submittedDate", ""),
        })
    return processed_data