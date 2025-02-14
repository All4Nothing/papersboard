import sqlite3
import pandas as pd

# 데이터베이스 파일 경로 (실제 경로로 변경)
db_path = "/Users/yongjoo/Desktop/papersboard/papers.db"

# CSV 저장 경로 (실제 경로로 변경)
csv_path = "/Users/yongjoo/Desktop/papersboard/papers_export.csv"

def export_papers_to_csv():
    """papers.db에서 논문 데이터를 CSV로 저장"""
    try:
        # 데이터베이스 연결
        conn = sqlite3.connect(db_path)

        # 논문 데이터 가져오기
        query = "SELECT title, abstract, url, domain_task, keywords FROM papers"
        df = pd.read_sql_query(query, conn)

        # 데이터베이스 연결 종료
        conn.close()

        # CSV 파일로 저장
        df.to_csv(csv_path, index=False, encoding="utf-8")

        print(f"✅ CSV 파일 저장 완료: {csv_path}")
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")

if __name__ == "__main__":
    export_papers_to_csv()