# app/api/advice.py (通义千问版本)

from openai import OpenAI
from flask import Blueprint, request, jsonify, current_app
from app.models import Transaction
from .decorators import token_required
from datetime import datetime

bp = Blueprint("advice", __name__)


@bp.route("/advice", methods=["POST"])
@token_required
def get_financial_advice(current_user):
    """根据用户指定时间范围的消费数据，生成AI财务建议 (由通义千问驱动)"""

    # 1. 初始化通义千问客户端
    try:
        client = OpenAI(
            api_key=current_app.config["DASHSCOPE_API_KEY"],
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
    except Exception as e:
        return jsonify(
            {"error": "AI service configuration failed", "details": str(e)}
        ), 500

    # 2. 获取并验证请求数据 (逻辑不变)
    data = request.get_json()
    start_date_str = data.get("start_date")
    end_date_str = data.get("end_date")

    if not start_date_str or not end_date_str:
        return jsonify({"error": "start_date and end_date are required"}), 400

    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

    # 3. 查询时间范围内的消费数据 (逻辑不变)
    transactions = Transaction.query.filter(
        Transaction.user_id == current_user.id,
        Transaction.transaction_date.between(start_date, end_date),
    ).all()

    if not transactions:
        return jsonify(
            {"advice": "📈 这段时间内没有消费记录，无法生成建议。继续保持！"}
        ), 200

    # 4. 构建 Prompt (逻辑不变，只是将结果喂给不同的模型)
    user_data_prompt = (
        f"我在 {start_date_str} 到 {end_date_str} 期间的消费数据如下：\n\n"
    )
    total_expense = 0
    expenses_by_category = {}

    for t in transactions:
        if t.type == "expense":
            category_name = t.category.name if t.category else "未分类"
            total_expense += t.amount
            if category_name not in expenses_by_category:
                expenses_by_category[category_name] = 0
            expenses_by_category[category_name] += t.amount

    user_data_prompt += f"总支出：{total_expense:.2f}元。\n"
    user_data_prompt += "各项支出分类如下：\n"
    for category, amount in expenses_by_category.items():
        user_data_prompt += f"- {category}: {amount:.2f}元\n"

    # 5. 调用 AI 模型并返回结果
    try:
        completion = client.chat.completions.create(
            model="qwen-plus",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "你是一位专业的财务规划师。"
                        "请根据用户提供的数据，为他提供一份简短、友好、口语化的财务分析和建议。"
                        "请注意：1. 分析主要消费领域。 2. 提出1-2个具体省钱建议。 3. 全文多使用 emoji。 4. 总结时给一些鼓励。"
                    ),
                },
                {"role": "user", "content": user_data_prompt},
            ],
        )

        advice_text = completion.choices[0].message.content
        return jsonify({"advice": advice_text})

    except Exception as e:
        return jsonify(
            {"error": "Failed to generate AI advice", "details": str(e)}
        ), 503
