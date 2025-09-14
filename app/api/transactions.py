# app/api/transactions.py (功能增强版)

from flask import Blueprint, request, jsonify
from app.models import Transaction, Category, User
from app import db
from .decorators import token_required
from datetime import datetime

bp = Blueprint("transactions", __name__)


# --- 创建交易 (保持不变) ---
@bp.route("/transactions", methods=["POST"])
@token_required
def create_transaction(current_user):
    data = request.get_json()
    required_fields = ["amount", "type", "transaction_date"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    if data["type"] == "expense" and "category_id" not in data:
        return jsonify({"error": "category_id is required for expense"}), 400

    try:
        new_transaction = Transaction(
            user_id=current_user.id,
            amount=data["amount"],
            type=data["type"],
            transaction_date=datetime.strptime(
                data["transaction_date"], "%Y-%m-%d"
            ).date(),
            notes=data.get("notes"),
            category_id=data.get("category_id"),
        )
        if new_transaction.type == "expense":
            category = Category.query.get(new_transaction.category_id)
            if not category:
                return jsonify({"error": "Category not found"}), 404
            if category.is_custom and category.user_id != current_user.id:
                return jsonify({"error": "Invalid category_id"}), 403

        db.session.add(new_transaction)
        db.session.commit()
        return jsonify(
            {"message": "Transaction created", "id": new_transaction.id}
        ), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred", "details": str(e)}), 500


# --- 获取交易列表 (保持不变) ---
@bp.route("/transactions", methods=["GET"])
@token_required
def get_transactions(current_user):
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    query = Transaction.query.filter_by(user_id=current_user.id).order_by(
        Transaction.transaction_date.desc(), Transaction.id.desc()
    )
    paginated_transactions = query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    transactions_list = []
    for t in paginated_transactions.items:
        transactions_list.append(
            {
                "id": t.id,
                "amount": str(t.amount),
                "type": t.type,
                "transaction_date": t.transaction_date.isoformat(),
                "notes": t.notes,
                "category_id": t.category_id,
                "category_name": t.category.name if t.category else None,
            }
        )
    return jsonify(
        {
            "items": transactions_list,
            "total_items": paginated_transactions.total,
            "total_pages": paginated_transactions.pages,
            "current_page": paginated_transactions.page,
            "has_next": paginated_transactions.has_next,
            "has_prev": paginated_transactions.has_prev,
        }
    )


# --- 【新增】获取单条交易记录 ---
@bp.route("/transactions/<int:id>", methods=["GET"])
@token_required
def get_transaction(current_user, id):
    transaction = Transaction.query.get_or_404(id)
    if transaction.user_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403
    return jsonify(
        {
            "id": transaction.id,
            "amount": str(transaction.amount),
            "type": transaction.type,
            "transaction_date": transaction.transaction_date.isoformat(),
            "notes": transaction.notes,
            "category_id": transaction.category_id,
        }
    )


# --- 【新增】更新一条交易记录 ---
@bp.route("/transactions/<int:id>", methods=["PUT"])
@token_required
def update_transaction(current_user, id):
    transaction = Transaction.query.get_or_404(id)
    if transaction.user_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    transaction.amount = data.get("amount", transaction.amount)
    transaction.type = data.get("type", transaction.type)
    transaction.transaction_date = (
        datetime.strptime(data.get("transaction_date"), "%Y-%m-%d").date()
        if data.get("transaction_date")
        else transaction.transaction_date
    )
    transaction.notes = data.get("notes", transaction.notes)
    transaction.category_id = data.get("category_id", transaction.category_id)

    db.session.commit()
    return jsonify({"message": "Transaction updated successfully"})


# --- 【新增】删除一条交易记录 ---
@bp.route("/transactions/<int:id>", methods=["DELETE"])
@token_required
def delete_transaction(current_user, id):
    transaction = Transaction.query.get_or_404(id)
    if transaction.user_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403

    db.session.delete(transaction)
    db.session.commit()
    return jsonify({"message": "Transaction deleted successfully"})
