# app/__init__.py (修正CORS配置的版本)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 将原来的 CORS(app) 替换为下面这行更详细的配置
    # 这会明确告诉浏览器，允许所有来源，并支持携带cookies等凭证
    CORS(app, supports_credentials=True)

    db.init_app(app)
    migrate.init_app(app, db)

    # --- 后面的蓝图等部分保持不变 ---
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

    from app import models
    from app import commands

    app.cli.add_command(commands.seed_command)

    @app.route("/test")
    def test_route():
        return "<h1>App is running!</h1>"

    return app
