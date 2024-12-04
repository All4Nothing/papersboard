from flask import Blueprint, jsonify

user_routes = Blueprint("user_routes", __name__)

# 사용자 정보 예시 데이터
users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"}
]

@user_routes.route("/users", methods=["GET"])
def get_users():
    return jsonify(users)

@user_routes.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = next((user for user in users if user["id"] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404