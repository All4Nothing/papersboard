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
    domain_task = db.Column(db.String, nullable=True)

def save_paper_to_db(paper_data):
    """
    주어진 논문 데이터를 데이터베이스에 저장합니다.
    """
    paper = Paper(
        title=paper_data["title"],
        abstract=paper_data["abstract"],
        authors=paper_data["authors"],
        published_date=paper_data["published_date"],
        source=paper_data["source"],
        url=paper_data["url"]
    )
    db.session.add(paper)
    db.session.commit()