import os
from dotenv import load_dotenv

# 定位项目根目录
basedir = os.path.abspath(os.path.dirname(__file__))
# 加载 .env 文件中的环境变量
load_dotenv(os.path.join(basedir, ".env"))


class Config:
    """
    基础配置类，包含所有环境共用的配置。
    """

    # 从 .env 文件中加载密钥，或者使用一个默认值
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"

    # 从 .env 文件中加载数据库URI，或者设置一个默认的SQLite数据库
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "app.db")

    # 关闭 SQLAlchemy 的事件通知系统，以节省资源
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DASHSCOPE_API_KEY = os.environ.get("DASHSCOPE_API_KEY")
