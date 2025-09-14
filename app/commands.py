import click
from flask.cli import with_appcontext
from app import db
from app.models import Category


@click.command("seed")
@with_appcontext
def seed_command():
    """向数据库中添加预设的消费类别"""

    default_categories = ["餐饮", "购物", "交通", "娱乐", "学习", "日用", "其他"]

    # 检查类别是否已存在，避免重复添加
    existing_categories = [
        c.name for c in Category.query.filter_by(is_custom=False).all()
    ]

    for cat_name in default_categories:
        if cat_name not in existing_categories:
            category = Category(name=cat_name, is_custom=False, user_id=None)
            db.session.add(category)
            print(f"Added default category: {cat_name}")

    db.session.commit()
    print("Default categories seeded.")
