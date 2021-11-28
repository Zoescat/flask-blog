from exts import db
from datetime import datetime

# 文章类型
class Article_type(db.Model):
    __table_args__ = {'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8mb4'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type_name = db.Column(db.String(20), nullable=False)
    articles=db.relationship('Article',backref='articletype')  

# 文章
class Article(db.Model):
    __table_args__ = {'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8mb4'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    pdatetime = db.Column(db.DateTime, default=datetime.now)
    click_num = db.Column(db.Integer, default=0)
    saveclick_num = db.Column(db.Integer, default=0)
    love_num = db.Column(db.Integer, default=0)
    # 外键 一对多 同步到数据库的外键关系,在多的一方加外键
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('article_type.id'), nullable=False)
    comments=db.relationship('Comment',backref='acticle')


# 评论
class Comment(db.Model):
    __table_args__ = {'mysql_engine' : 'InnoDB', 'mysql_charset' : 'utf8mb4'}
    # 自定义表名
    __tablename__='comment'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    cdatetime = db.Column(db.DateTime, default=datetime.now)

    def __str__(self):
        return self.comment
