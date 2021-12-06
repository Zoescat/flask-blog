from flask import Flask
import settings
from exts import db,bootstrap
from apps.user.views import user_bp,index_bp
from apps.article.views import article_bp




def create_app():
    # app是一个核心对象
    app = Flask(__name__, template_folder='../templates',static_folder='../static')
    # 加载配置
    app.config.from_object(settings.DevelopmentConfig)
    # 将db对象与app进行关联,初始化配置db
    db.init_app(app=app)
    # 初始化bootstrap
    bootstrap.init_app(app=app)
    # 蓝图 是路由的另外一种表示方式
    # 将蓝图对象绑定到app上
    app.register_blueprint(user_bp)
    app.register_blueprint(index_bp)
    app.register_blueprint(article_bp)

    # print(app.url_map)
    return app
