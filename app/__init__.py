# app/__init__.py (最终修正版)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

# 在这里，我们只创建扩展实例，不进行任何从 app 子模块的导入
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    """
    应用工厂函数。
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 将扩展实例与 app 绑定
    db.init_app(app)
    migrate.init_app(app, db)

    # --- 将所有的蓝图、模型、命令导入都放在函数内部 ---
    from app.api.auth import bp as auth_bp

    app.register_blueprint(auth_bp, url_prefix="/api")

    from app.api.transactions import bp as trans_bp

    app.register_blueprint(trans_bp, url_prefix="/api")

    from app.api.categories import bp as cat_bp

    app.register_blueprint(cat_bp, url_prefix="/api")

    from app.api.dashboard import bp as dash_bp

    app.register_blueprint(dash_bp, url_prefix="/api")

    from app.api.advice import bp as advice_bp

    app.register_blueprint(advice_bp, url_prefix="/api")

    # 这两个导入对于让 Flask-Migrate 和 SQLAlchemy 发现模型至关重要
    from app import models
    from app import commands

    app.cli.add_command(commands.seed_command)

    @app.route("/test")
    def test_route():
        return "<h1>App is running!</h1>"

    return app
