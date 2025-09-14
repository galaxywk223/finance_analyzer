from app import create_app

# 调用应用工厂，创建 app 实例
app = create_app()

# 这个 if __name__ == '__main__': 块是 Python 脚本的常用入口点
# 但对于 Flask 应用，推荐使用 'flask run' 命令启动，
# 它会自动寻找名为 app 或 create_app 的工厂。
# 所以这个文件现在非常简单。
