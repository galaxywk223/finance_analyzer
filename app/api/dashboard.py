from flask import Blueprint, jsonify
from app.models import Transaction, Category
from app import db
from .decorators import token_required
from sqlalchemy import func
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from decimal import Decimal

bp = Blueprint("dashboard", __name__)


@bp.route("/dashboard/summary", methods=["GET"])
@token_required
def get_dashboard_summary(current_user):
    """获取仪表盘所需的全部汇总数据"""

    # --- 1. 日期计算 ---
    today = datetime.utcnow().date()
    start_of_current_month = today.replace(day=1)
    start_of_next_month = start_of_current_month + relativedelta(months=1)
    start_of_last_month = start_of_current_month - relativedelta(months=1)
    thirty_days_ago = today - timedelta(days=29)

    # --- 2. 当月收支与结余 (修正默认值为 Decimal) ---
    current_month_income_query = db.session.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == current_user.id,
        Transaction.type == "income",
        Transaction.transaction_date >= start_of_current_month,
        Transaction.transaction_date < start_of_next_month,
    ).scalar() or Decimal("0.0")

    current_month_expense_query = db.session.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == current_user.id,
        Transaction.type == "expense",
        Transaction.transaction_date >= start_of_current_month,
        Transaction.transaction_date < start_of_next_month,
    ).scalar() or Decimal("0.0")

    # --- 3. 与上月消费对比 (修正默认值为 Decimal) ---
    last_month_expense_query = db.session.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == current_user.id,
        Transaction.type == "expense",
        Transaction.transaction_date >= start_of_last_month,
        Transaction.transaction_date < start_of_current_month,
    ).scalar() or Decimal("0.0")

    # --- 4. 按消费类别统计 (饼图数据) ---
    category_expense_query = (
        db.session.query(Category.name, func.sum(Transaction.amount).label("total"))
        .join(Category)
        .filter(
            Transaction.user_id == current_user.id,
            Transaction.type == "expense",
            Transaction.transaction_date >= start_of_current_month,
            Transaction.transaction_date < start_of_next_month,
        )
        .group_by(Category.name)
        .order_by(func.sum(Transaction.amount).desc())
        .all()
    )

    # --- 5. 最近30天消费趋势 (折线图数据) ---
    daily_trend_query = (
        db.session.query(
            func.date(Transaction.transaction_date).label("date"),
            func.sum(Transaction.amount).label("total"),
        )
        .filter(
            Transaction.user_id == current_user.id,
            Transaction.type == "expense",
            Transaction.transaction_date >= thirty_days_ago,
            Transaction.transaction_date <= today,
        )
        .group_by(func.date(Transaction.transaction_date))
        .order_by(func.date(Transaction.transaction_date))
        .all()
    )

    # --- 6. 组装最终的 JSON 响应 ---
    summary = {
        "current_month_summary": {
            "income": f"{current_month_income_query:.2f}",
            "expense": f"{current_month_expense_query:.2f}",
            "balance": f"{(current_month_income_query - current_month_expense_query):.2f}",
        },
        "last_month_comparison": {
            "last_month_expense": f"{last_month_expense_query:.2f}",
            "current_month_expense": f"{current_month_expense_query:.2f}",
        },
        "category_breakdown": [
            {"category": name, "total": f"{total:.2f}"}
            for name, total in category_expense_query
        ],
        "daily_trend_last_30_days": [
            {"date": date, "total": f"{total:.2f}"} for date, total in daily_trend_query
        ],
    }

    return jsonify(summary)
