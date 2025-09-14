from flask import Blueprint, request, jsonify
from app.models import Transaction, Category
from app import db
from .decorators import token_required
from datetime import datetime

bp = Blueprint("transactions", __name__)


@bp.route("/transactions", methods=["POST"])
@token_required
def create_transaction(current_user):
    """
    创建一笔新的交易记录 (支出或收入)
    这个函数接收一个 current_user 参数，由 @token_required 装饰器提供
    """
    data = request.get_json()

    # --- 基本数据校验 ---
    required_fields = ["amount", "type", "transaction_date"]
    if not all(field in data for field in required_fields):
        return jsonify(
            {"error": "Missing required fields (amount, type, transaction_date)"}
        ), 400

    # 如果是支出，则类别ID是必需的
    if data["type"] == "expense" and "category_id" not in data:
        return jsonify({"error": "category_id is required for expense type"}), 400

    # --- 写入数据库 ---
    try:
        new_transaction = Transaction(
            owner=current_user,  # 直接关联解码出的用户信息
            amount=data["amount"],
            type=data["type"],
            transaction_date=datetime.strptime(
                data["transaction_date"], "%Y-%m-%d"
            ).date(),
            notes=data.get("notes"),  # .get() 方法允许字段为空
            category_id=data.get("category_id"),  # 如果是收入，则此项可能不存在
        )

        # 验证 category_id 是否有效 (如果是支出)
        if new_transaction.type == "expense":
            category = Category.query.get(new_transaction.category_id)
            if not category:
                return jsonify({"error": "Category not found"}), 404
            # 确保用户不能使用其他用户创建的私有分类
            if category.is_custom and category.creator != current_user:
                return jsonify({"error": "Invalid category_id"}), 403  # Forbidden

        db.session.add(new_transaction)
        db.session.commit()

        return jsonify(
            {"message": "Transaction created successfully", "id": new_transaction.id}
        ), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred", "details": str(e)}), 500


@bp.route("/transactions", methods=["GET"])
@token_required
def get_transactions(current_user):
    """获取当前用户的交易记录列表，支持筛选和分页"""

    # 获取查询参数
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    start_date_str = request.args.get("start_date")
    end_date_str = request.args.get("end_date")
    trans_type = request.args.get("type")

    # 基础查询：只查找属于当前用户的记录
    query = Transaction.query.filter_by(owner=current_user)

    # 根据查询参数动态添加筛选条件
    if start_date_str:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        query = query.filter(Transaction.transaction_date >= start_date)

    if end_date_str:
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        query = query.filter(Transaction.transaction_date <= end_date)

    if trans_type in ["income", "expense"]:
        query = query.filter_by(type=trans_type)

    # 按交易日期倒序排序
    query = query.order_by(Transaction.transaction_date.desc(), Transaction.id.desc())

    # 执行分页查询
    paginated_transactions = query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    transactions = paginated_transactions.items

    # 格式化输出
    transactions_list = []
    for t in transactions:
        transactions_list.append(
            {
                "id": t.id,
                "amount": str(t.amount),  # DECIMAL 类型建议转为字符串
                "type": t.type,
                "transaction_date": t.transaction_date.isoformat(),
                "notes": t.notes,
                "category_id": t.category_id,
                "category_name": t.category.name
                if t.category
                else None,  # 附加类别名称
            }
        )

    # 构造响应体
    response = {
        "items": transactions_list,
        "total_items": paginated_transactions.total,
        "total_pages": paginated_transactions.pages,
        "current_page": paginated_transactions.page,
        "has_next": paginated_transactions.has_next,
        "has_prev": paginated_transactions.has_prev,
    }

    return jsonify(response)
