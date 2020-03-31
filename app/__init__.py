from flask import Flask
import configs
from app.db_mysql import db
from app.view import xiaojiejie
from flask_bootstrap import Bootstrap

def create_app():
    app = Flask(__name__)

    # 加载配置
    app.config.from_object(configs)
    # Install our Bootstrap extension
    bootstrap = Bootstrap(app)
    # Because we're security-conscious developers, we also hard-code disabling
    # the CDN support (this might become a default in later versions):
    app.config['BOOTSTRAP_SERVE_LOCAL'] = True

    # 初始化db
    db.app = app
    db.init_app(app)
    # 注册蓝图
    app.register_blueprint(xiaojiejie)

    return app