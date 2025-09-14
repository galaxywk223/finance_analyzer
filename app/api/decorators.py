# app/api/decorators.py (修正后的版本)

from functools import wraps
import jwt
from flask import request, jsonify, current_app
from app.models import User


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None  # <--- 关键修正：在这里初始化 token 变量

        # 检查 Token 是否在请求头中
        if "Authorization" in request.headers:
            # 请求头的格式通常是 'Bearer <token>'
            auth_header = request.headers["Authorization"]
            parts = auth_header.split()

            # 确保请求头格式正确 (Bearer a.b.c)
            if len(parts) == 2 and parts[0].lower() == "bearer":
                token = parts[1]

        if not token:
            return jsonify({"error": "Token is missing or header is malformed!"}), 401

        try:
            # 解码 Token，验证其有效性
            data = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )
            # 从 Token 中获取用户 ID，并查询数据库找到该用户
            current_user = User.query.get(data["sub"])
            if not current_user:
                return jsonify({"error": "User not found for this token!"}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired!"}), 401
        except Exception as e:
            # 我们不再需要那个 print 语句了，可以删掉
            return jsonify({"error": "Token is invalid!", "details": str(e)}), 401

        # 将查询到的用户信息传递给被装饰的路由函数
        return f(current_user, *args, **kwargs)

    return decorated
