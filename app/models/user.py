import bcrypt
from datetime import datetime
from app import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # 定义关系: 一个用户可以有多条交易记录和多个自定义分类
    transactions = db.relationship("Transaction", backref="owner", lazy=True)
    categories = db.relationship("Category", backref="creator", lazy=True)

    def set_password(self, password):
        """使用 bcrypt 对密码进行哈希加密"""
        # A salt is generated automatically by bcrypt
        self.password_hash = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

    def check_password(self, password):
        """校验密码是否正确"""
        return bcrypt.checkpw(
            password.encode("utf-8"), self.password_hash.encode("utf-8")
        )

    def __repr__(self):
        return f"<User {self.username}>"
