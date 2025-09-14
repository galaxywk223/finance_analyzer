# app/api/categories.py (功能增强版)

from flask import Blueprint, request, jsonify
from app.models import Category, Transaction
from app import db
from .decorators import token_required

bp = Blueprint("categories", __name__)


# --- 获取分类列表 (逻辑微调，确保 user_id 正确) ---
@bp.route("/categories", methods=["GET"])
@token_required
def get_categories(current_user):
    default_categories = Category.query.filter_by(is_custom=False).all()
    user_categories = Category.query.filter_by(user_id=current_user.id).all()
    categories_list = []
    for c in default_categories + user_categories:
        categories_list.append({"id": c.id, "name": c.name, "is_custom": c.is_custom})
    return jsonify(categories_list)


# --- 创建分类 (逻辑微调，确保 user_id 正确) ---
@bp.route("/categories", methods=["POST"])
@token_required
def create_category(current_user):
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Missing category name"}), 400

    new_category = Category(name=data["name"], is_custom=True, user_id=current_user.id)
    db.session.add(new_category)
    db.session.commit()
    return jsonify(
        {
            "message": "Category created",
            "id": new_category.id,
            "name": new_category.name,
            "is_custom": True,
        }
    ), 201


# --- 【新增】更新一个分类 ---
@bp.route("/categories/<int:id>", methods=["PUT"])
@token_required
def update_category(current_user, id):
    category = Category.query.get_or_404(id)
    # 安全检查：确保是用户自己的自定义分类
    if not category.is_custom or category.user_id != current_user.id:
        return jsonify({"error": "Unauthorized to update this category"}), 403

    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Missing category name"}), 400

    category.name = data["name"]
    db.session.commit()
    return jsonify({"message": "Category updated successfully"})


# --- 【新增】删除一个分类 ---
@bp.route("/categories/<int:id>", methods=["DELETE"])
@token_required
def delete_category(current_user, id):
    category = Category.query.get_or_404(id)
    # 安全检查：确保是用户自己的自定义分类
    if not category.is_custom or category.user_id != current_user.id:
        return jsonify({"error": "Unauthorized to delete this category"}), 403

    # 在删除分类前，将使用该分类的交易记录的 category_id 设为 null
    Transaction.query.filter_by(category_id=id).update({"category_id": None})

    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Category deleted successfully"})
