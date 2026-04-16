import sqlite3
import os
from flask import Flask


def init_db(app):
    """讀取 schema.sql 並初始化 SQLite 資料庫"""
    db_path = os.path.join(app.instance_path, 'database.db')
    schema_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'schema.sql')

    os.makedirs(app.instance_path, exist_ok=True)

    with sqlite3.connect(db_path) as conn:
        with open(schema_path, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
    print("✅ 資料庫初始化完成！")


def create_app():
    """初始化並配置 Flask 應用程式"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev-secret-key'),
    )

    # 初始化資料庫指令
    with app.app_context():
        init_db(app)

    # 註冊所有的 Blueprint 路由
    from app.routes.main import bp as main_bp
    from app.routes.auth import bp as auth_bp
    from app.routes.fortune import bp as fortune_bp
    from app.routes.history import bp as history_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(fortune_bp)
    app.register_blueprint(history_bp)

    return app
