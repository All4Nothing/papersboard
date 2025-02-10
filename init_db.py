'''
	1.	Flask 앱을 생성하고 데이터베이스를 설정한다.
	2.	앱 컨텍스트를 활성화하여 Flask가 데이터베이스와 상호작용할 수 있도록 한다.
	3.	db.create_all()을 호출하여 데이터베이스의 테이블을 생성한다.
'''
from app import create_app
from app.services.database import db

app = create_app()

with app.app_context():
    db.create_all()