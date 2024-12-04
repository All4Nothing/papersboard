from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def recommend_papers(user_input, papers, top_n=5):
    """
    논문 데이터를 기반으로 사용자가 선택한 논문과 유사한 논문을 추천합니다.
    
    Args:
        user_input (str): 사용자가 입력한 키워드 또는 관심 논문의 제목/초록.
        papers (list of dict): 논문 리스트. 각 논문은 {"title": ..., "abstract": ...} 형태의 딕셔너리.
        top_n (int): 추천할 논문 개수.

    Returns:
        list of dict: 추천된 논문의 리스트.
    """
    # 논문 제목과 초록 결합
    documents = [f"{paper['title']} {paper['abstract']}" for paper in papers]
    documents.append(user_input)  # 사용자의 입력 추가

    # TF-IDF 벡터화
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)

    # 코사인 유사도 계산
    cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])  # 마지막 벡터(사용자 입력)와 비교
    similarity_scores = cosine_sim.flatten()

    # 유사도 점수를 기준으로 상위 N개의 논문 선택
    top_indices = similarity_scores.argsort()[-top_n:][::-1]  # 유사도 높은 순으로 정렬
    recommended_papers = [papers[i] for i in top_indices]

    return recommended_papers