import psycopg2
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Paper(db.Model):
    __tablename__ = 'papers'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    abstract = db.Column(db.Text, nullable=False)
    authors = db.Column(db.String, nullable=True)
    published_date = db.Column(db.DateTime, nullable=True)
    source = db.Column(db.String, nullable=True)
    url = db.Column(db.String, unique=True, nullable=False)

    

def save_paper_to_db(paper):
    """
    논문 정보를 데이터베이스에 저장합니다.
    """
    connection = psycopg2.connect(
        dbname="dlmonitor",
        user="your_user",
        password="your_password",
        host="localhost",
        port="5432"
    )
    cursor = connection.cursor()

    query = """
    INSERT INTO papers (title, abstract, authors, published_date, source, url)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (url) DO NOTHING;
    """
    data = (
        paper["title"],
        paper["summary"],
        ", ".join(paper["authors"]),
        paper["published"],
        "arxiv",
        paper["url"],
    )
    cursor.execute(query, data)
    connection.commit()
    cursor.close()
    connection.close()