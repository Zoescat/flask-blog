import os


# 定义一个配置类
class Config:
    ENV = 'development'
    DEBUG = True
    # 
    # mysql+pymysql://username:password@hostip:port/databasename
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://zoe_learn_sql:Hello_11@oook.fun:3306/zoe_flask_blog'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@192.168.50.7:3306/zoe_flask_blog?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_ECHO=True
    # session的secret_key
    SECRET_KEY='xiaoweiba11'
    # 项目路径
    BASE_DIR=os.path.dirname(os.path.abspath(__file__))
    # 静态文件夹的路径
    STATIC_DIR=os.path.join(BASE_DIR,'static')
    # template 的路径
    TEMPLATE_DIR=os.path.join(BASE_DIR,'template')
    # 头像的上传目录
    UPLOAD_ICON_DIR=os.path.join(STATIC_DIR,'upload/icon')
    # 相册的上传目录
    UPLOAD_PHOTO_DIR=os.path.join(STATIC_DIR,'upload/photo')
                
# 开发环境
class DevelopmentConfig(Config):
    ENV = 'development'

# 生产环境


class ProductionConfig(Config):
    ENV = 'production'
    DEBUG = False

if __name__ == '__main__':
    print(Config.BASE_DIR)
    # print(os.path.abspath(__file__))
    print(Config.STATIC_DIR)
    print(Config.UPLOAD_ICON_DIR)