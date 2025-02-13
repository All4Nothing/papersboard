from app.services.database import db

class Paper(db.Model):
    __tablename__ = 'papers'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    abstract = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text, nullable=True)
    authors = db.Column(db.String, nullable=True)
    published_date = db.Column(db.DateTime, nullable=True)
    source = db.Column(db.String, nullable=True)
    url = db.Column(db.String, unique=True, nullable=False)
    domain_task = db.Column(db.String, nullable=True)
    keywords = db.Column(db.String, nullable=True)