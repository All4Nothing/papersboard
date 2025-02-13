from app.services.database import db
from datetime import datetime

class LastUpdate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    updated_at = db.Column(db.DateTime, default=datetime.now, nullable=False)