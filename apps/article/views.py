from flask import Blueprint, render_template, request, redirect, url_for, g, jsonify, session
from apps.user.models import User
from apps.article.models import Article, Article_type, Comment
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
        print('content=', content)
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


# 文章详情
@article_bp.route('/detail')
def article_detail():
    # 通过id获取文章对象
    article_id = request.args.get('aid')
    article = Article.query.get(article_id)
    # 获取文章分类
    types = Article_type.query.all()
    print('types=', types)
    # 登录用户
    user = None
    user_id = session.get('uid', None)
    if user_id:
        user = User.query.get(user_id)
    # 单独查询评论
    page = int(request.args.get('page', 1))
    comments = Comment.query.filter(Comment.article_id == article_id)\
        .order_by(-Comment.cdatetime)\
        .paginate(page=page, per_page=5)

    return render_template('article/detail.html', article=article, types=types, user=user, comments=comments)


# 文章点赞数
@article_bp.route('/love')
def article_love():
    # 通过id获取文章对象
    article_id = request.args.get('aid')
    tag = request.args.get('tag')
    article = Article.query.get(article_id)
    print('tag=', tag)
    if tag == '1':
        article.love_num -= 1
    else:
        article.love_num += 1
    db.session.commit()
    return jsonify(num=article.love_num)


# 文章评论
@article_bp.route('/add_comment', methods=['GET', 'POST'])
def article_comment():
    if request.method == 'POST':
        comment_content = request.form.get('comment')
        user_id = g.user.id
        article_id = request.form.get('aid')
        # 评论模型
        comment = Comment()
        comment.comment = comment_content
        comment.user_id = user_id
        comment.article_id = article_id
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('article.article_detail')+"?aid="+article_id)

    return redirect(url_for('user.index'))
