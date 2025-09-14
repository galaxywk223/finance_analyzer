import jwt
from flask import Blueprint, request, jsonify, current_app
from app.models import User
from app import db
from datetime import datetime, timedelta, timezone

# 创建一个名为 'auth' 的蓝图
bp = Blueprint("auth", __name__)


@bp.route("/register", methods=["POST"])
def register():
    """用户注册接口"""
    data = request.get_json()
    if not data or not "username" in data or not "password" in data:
        return jsonify({"error": "Missing username or password"}), 400

    username = data["username"]
    password = data["password"]

    # 检查用户名是否已存在
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 409  # 409 Conflict

    # 创建新用户
    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201  # 201 Created


# app/api/auth.py (修正后的 login 函数)


@bp.route("/login", methods=["POST"])
def login():
    """用户登录接口"""
    data = request.get_json()
    if not data or not "username" in data or not "password" in data:
        return jsonify({"error": "Missing username or password"}), 400

    username = data["username"]
    password = data["password"]

    user = User.query.filter_by(username=username).first()

    # 验证用户和密码
    if user is None or not user.check_password(password):
        return jsonify({"error": "Invalid username or password"}), 401

    # 生成 JWT Token
    token_payload = {
        "sub": str(user.id),  # 确保 sub 是字符串，并且这是唯一的 'sub' 键
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(hours=24),
    }

    token = jwt.encode(
        token_payload, current_app.config["SECRET_KEY"], algorithm="HS256"
    )

    return jsonify({"token": token})
