from flask import Blueprint, render_template, request, redirect, url_for, g, jsonify
from apps.user.models import User
from apps.article.models import Article, Article_type
from exts import db
import flask


article_bp = Blueprint('article', __name__, url_prefix='/article')


# 自定义过滤器
@article_bp.app_template_filter('cdecode')
def content_decode(content):
    content = content.decode('utf-8')
    return content


# 发布文章
@article_bp.route('/publish', methods=['GET', 'POST'])
def publish_article():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        type_id = request.form.get('type')
        print('content=',content)
        # 添加文章
        article = Article()
        article.title = title
        article.content = content
        article.type_id = type_id
        article.user_id = g.user.id
        print(article.__dict__)
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('user.index'))
  


# 文章明细
@article_bp.route('/detail')
def article_detail():
    # 通过id获取文章对象
    article_id = request.args.get('aid')
    article = Article.query.get(article_id)
    # 获取文章分类
    types = Article_type.query.all()
    print('types=',types)
    return render_template('article/detail.html', article=article, types=types)


# 文章点赞数
@article_bp.route('/love')
def article_love():
    # 通过id获取文章对象
    article_id = request.args.get('aid')
    tag = request.args.get('tag')
    article = Article.query.get(article_id)
    print('tag=',tag)
    if tag == '1':
        article.love_num -= 1
    else:
        article.love_num += 1
    db.session.commit()
    return jsonify(num=article.love_num)
