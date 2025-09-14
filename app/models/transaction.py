from app import db
from datetime import date


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    type = db.Column(db.String(10), nullable=False)  # 'income' or 'expense'
    transaction_date = db.Column(db.Date, nullable=False, default=date.today)
    notes = db.Column(db.Text, nullable=True)

    # 外键，关联到用户ID。一条记录必须属于一个用户。
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    # 外键，关联到类别ID。收入记录此项为空。
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=True)

    def __repr__(self):
        return f"<Transaction {self.id}>"
