# ORM 类--->表
# 类对象--->表中的一条数据
from exts import db
from datetime import datetime


# 用户模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(11), unique=True)
    email = db.Column(db.String(30))
    icon = db.Column(db.String(100))
    isdelete = db.Column(db.Boolean, default=False)
    # 注册时间->默认获取系统的当前时间
    rdatetime = db.Column(db.DateTime, default=datetime.now)
    # 增加一个字段articles
    articles = db.relationship('Article', backref='user')  # backref 反向引用
    comments = db.relationship('Comment', backref='user')

    def __str__(self):
        return self.username



# 相册模型
class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    photo_name = db.Column(db.String(80), nullable=False)
    photo_datetime = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)

def __str__(self):
    return self.photo_name