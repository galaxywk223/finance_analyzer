from app import db


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    is_custom = db.Column(db.Boolean, nullable=False, default=False)

    # 外键，关联到用户ID。预设类别此项为空。
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    # 定义关系: 一个分类下可以有多条交易记录
    transactions = db.relationship("Transaction", backref="category", lazy=True)

    def __repr__(self):
        return f"<Category {self.name}>"
