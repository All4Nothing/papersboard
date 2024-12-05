from flask import Blueprint, render_template, request, jsonify
from transformers import pipeline
from app.services.arxiv_service import fetch_latest_papers, categorize_papers
from app.services.nlp_service import summarize_paper_abstracts, generate_weekly_report

main_routes = Blueprint("main_routes", __name__)

TASKS = [
    "Reinforcement Learning",
    "Computer Vision",
    "Natural Language Processing",
    "Recommendation System"
]

@main_routes.route("/")
def index():
    # 메인 페이지에서 task 버튼을 표시
    papers = fetch_latest_papers()
    category_counts = categorize_papers(papers)
    summaries = summarize_paper_abstracts(papers)
    weekly_report = generate_weekly_report(summaries)
    return render_template("index.html", category_counts=category_counts, report=weekly_report, tasks=TASKS)

@main_routes.route("/results", methods=["POST"])
def results():
    # 사용자 선택한 task 리스트 가져오기
    selected_tasks = request.form.getlist("tasks")
    papers_by_task = {}

    # 각 task에 대해 관련 논문 검색
    for task in selected_tasks:
        papers_by_task[task] = fetch_latest_papers(task, max_results=10, last_days=2)["data"]

    # 결과 페이지 렌더링
    return render_template("results.html", selected_tasks=selected_tasks, papers_by_task=papers_by_task)

@main_routes.route("/api/report", methods=["GET"])
def api_report():
    papers = fetch_latest_papers()  # 최신 논문 가져오기
    summaries = summarize_paper_abstracts(papers)  # 논문 요약 생성
    report = generate_weekly_report(summaries)  # 최종 보고서 생성
    return jsonify({"report": report})