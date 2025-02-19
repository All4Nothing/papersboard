from sqlalchemy import create_engine
import os


DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        print("✅ Database 연결 성공")
except Exception as e:
    print(f"❌ Database 연결 실패: {e}")