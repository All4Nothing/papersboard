import sqlite3
import pandas as pd

db_path = "/Users/yongjoo/Desktop/papersboard/papers.db"
conn = sqlite3.connect(db_path)

query = "SELECT * FROM papers"
df = pd.read_sql(query, conn)
conn.close()

print(df.head())

df.to_csv("/Users/yongjoo/Desktop/papersboard/db_dataset.csv", index=False, encoding="utf-8")
print("✅ Saved as CSV")