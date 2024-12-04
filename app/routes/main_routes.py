from flask import Blueprint, render_template, request
from app.services.arxiv_service import fetch_latest_papers

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
    return render_template("index.html", tasks=TASKS)

@main_routes.route("/results", methods=["POST"])
def results():
    # 사용자 선택한 task 리스트 가져오기
    selected_tasks = request.form.getlist("tasks")
    papers_by_task = {}

    # 각 task에 대해 관련 논문 검색
    for task in selected_tasks:
        papers_by_task[task] = fetch_latest_papers(task, max_results=10)["data"]

    # 결과 페이지 렌더링
    return render_template("results.html", selected_tasks=selected_tasks, papers_by_task=papers_by_task)