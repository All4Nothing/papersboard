import requests

url = "http://127.0.0.1:5000/api/category_counts"  # 정확한 URL 사용
response = requests.get(url)

if response.status_code == 200:
    print("API 응답 성공:", response.json())
else:
    print("API 응답 실패:", response.status_code)