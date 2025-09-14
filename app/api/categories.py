from flask import Blueprint, request, jsonify
from app.models import Category
from app import db
from .decorators import token_required

bp = Blueprint("categories", __name__)


@bp.route("/categories", methods=["GET"])
@token_required
def get_categories(current_user):
    """获取所有可用类别（系统预设 + 用户自定义）"""

    # 获取系统预设类别
    default_categories = Category.query.filter_by(is_custom=False).all()

    # 获取当前用户的自定义类别
    user_categories = Category.query.filter_by(creator=current_user).all()

    # 格式化输出
    categories_list = [
        {"id": c.id, "name": c.name, "is_custom": c.is_custom}
        for c in (default_categories + user_categories)
    ]

    return jsonify(categories_list)


@bp.route("/categories", methods=["POST"])
@token_required
def create_category(current_user):
    """创建用户自定义类别"""
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Missing category name"}), 400

    new_category = Category(name=data["name"], is_custom=True, creator=current_user)
    db.session.add(new_category)
    db.session.commit()

    return jsonify(
        {
            "message": "Category created successfully",
            "id": new_category.id,
            "name": new_category.name,
        }
    ), 201
