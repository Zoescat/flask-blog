from re import template
from flask import Blueprint, render_template, request, jsonify, session, g
from flask.helpers import url_for
from flask_sqlalchemy import Pagination
from werkzeug.utils import redirect, secure_filename
from werkzeug.wrappers import response
from apps.article.models import Article, Article_type
from apps.user.models import AboutMe, User, Photo,MessageBoard
from apps.user.smssend import SmsSendAPIDemo
from exts import db
from werkzeug.security import check_password_hash, generate_password_hash
import os
from settings import Config
from pathlib import PurePath, PurePosixPath
from apps.utils.util import upload_qiniu_photo,delete_qiniu


user_bp = Blueprint('user', __name__, url_prefix='/user')
required_login_list = ['/user/center', 
                       '/user/change',
                       '/article/publish',
                       '/user/upload_photo',
                       '/article/add_comment',
                       '/user/about_me',
                       '/user/showabout'
                       ]


# flask钩子函数
#
@user_bp.before_app_first_request
def first_request():
    pass
    # print('before_app_first_request')


# 钩子函数
@user_bp.before_app_request
def before_request1():
    # print('before_request1before_request1', request.path)
    if request.path in required_login_list:
        id = session.get('uid')
        if not id:
            return render_template('user/login.html')
        else:
            user = User.query.get(id)
            # g对象，本次请求的对象
            g.user = user


@user_bp.after_app_request
def after_request_test(response):
    response.set_cookie('a', 'bbbb', max_age=19)
    # print('after_request_test')
    return response


@user_bp.teardown_app_request
def teardown_request_test(response):
    # print('teardown_request_test')
    return response


# 自定义过滤器
# @user_bp.app_template_filter('cdecode')
# def content_cdecode(content):
#     content=content.decode('utf-8')
#     return content[:200]


# 首页
@user_bp.route('/')
def index():
    # 1.cookie的获取方式
    # uid = request.cookies.get('uid', None)
    # 接收页码数
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 5))
    # 获取文章列表
    pagination = Article.query.order_by(
        -Article.pdatetime).paginate(page=page, per_page=per_page)
    # print(pagination.items)
    # print(pagination.page)   # 当前的页码数
    # print(pagination.prev_num)   # 当前页的前一个页码数
    # print(pagination.next_num)   # 当前页的后一个页码数
    # print(pagination.has_next)  # True
    # print(pagination.has_prev)  # True
    # print(pagination.pages)   # 总共有几页
    # print(pagination.total)   # 总的记录tiaoshu
    # 获取分类列表
    types = Article_type.query.all()
    # 2.session的获取方式
    uid = session.get('uid')
    # 判断用户是否登录
    if uid:
        user = User.query.get(uid)
        return render_template('user/index.html', user=user, pagination=pagination, types=types)
    else:
        return render_template('user/index.html', pagination=pagination, types=types)


# 用户注册
@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        phone = request.form.get('phone')
        email = request.form.get('email')
        if password == repassword:
            # 1.找到模型类，并创建对象
            user = User()
            # 2.给对象的属性赋值
            user.username = username
            # 使用自带的函数实现加密
            user.password = generate_password_hash(password)
            user.phone = phone
            user.email = email
            # 添加数据库
            # 3.将user对象添加到session中
            db.session.add(user)
            # 4.提交数据
            db.session.commit()
            # 重定向到用户中心
            return redirect(url_for('user.index'))
        else:
            return '两次密码不一致'
    return render_template('user/register.html')


# 手机号码验证 user.check_phone
@user_bp.route('/checkphone', methods=['GET', 'POST'])
def check_phone():
    phone = request.args.get('phone')
    user = User.query.filter(User.phone == phone).all()
    print('打印结果为：', user)
    if len(user) > 0:
        return jsonify(code=400, msg='该号码已注册')
    else:
        return jsonify(code=200, msg='该号码可以使用')


# 用户登录
@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        f = request.args.get('f')
        # 用户名和密码的登录
        if f == '1':
            username = request.form.get('username')
            password = request.form.get('password')
            # print('---->username是', username)
            # print('---->password是', password)
            users = User.query.filter(User.username == username).all()
            print(f'len(users) = {len(users)}')
            for user in users:
                # 如果flag=True表示匹配，否则密码不匹配
                flag = check_password_hash(user.password, password)
                print(f'====>user {user} - flag {flag}')
                if flag:
                    # 1.cookie实现机制
                    # response = redirect(url_for('user.index'))
                    # response.set_cookie('uid', str(user.id), max_age=1800)
                    # return response
                    # 2.session实现机制,session当成字典使用
                    session['uid'] = user.id
                    return redirect(url_for('user.index'))
        # 2.手机号码与验证码的登录
        elif f == '2':
            code = request.form.get('code')
            phone = request.form.get('phone')
            print(code, type(code))
            print(phone)
            # 验证验证码
            valid_code = session.get(phone)
            print('---->', valid_code, type(valid_code))
            if code == valid_code:
                # 查询数据库
                user = User.query.filter(User.phone == phone).first()
                print('user的内容是', user)
                if user:
                    # 登录成功
                    session['uid'] = user.id
                    return redirect(url_for('user.index'))
                else:
                    print('此号码未注册', phone)
                    return render_template('user/login.html', msg='此号码未注册')
            else:
                return render_template('user/login.html', msg='验证码错误')
    return render_template('user/login.html')


# 发送短信息
# SecretId：e1cac23a82cde32afda3fb2f5d388c58
# SecretKey：f605d4b5adfc7287b0292530e1a03d49
# businessId：faa5e0c414ec45d9b43be5f11a4975a6
@user_bp.route('/sendMsg')
def send_message():
    phone = request.args.get('phone')
    # 需要补充验证手机号码是否注册，去数据库查询

    code = sms_send(phone)
    session[phone] = code
    return jsonify(code=200, msg='短信发送成功')

    # if ret is not None:
    #     if ret["code"] == 200:
    #         taskId = ret["data"]["taskId"]
    #         print("taskId = %s" % taskId)
    #         session[phone]="123456"
    #         return jsonify(code=200,msg='短信发送成功')
    #     else:
    #         print ("ERROR: ret.code=%s,msg=%s" % (ret['code'], ret['msg']))
    #         return jsonify(code=400,msg='短信发送失败')


def sms_send(phone):
    # SECRET_ID = 'e1cac23a82cde32afda3fb2f5d388c58'    # 产品密钥ID 产品标识
    # SECRET_KEY = 'f605d4b5adfc7287b0292530e1a03d49'   # 产品私有秘钥，服务端生成签名信息使用
    # BUSINESS_ID = 'faa5e0c414ec45d9b43be5f11a4975a6'  # 业务ID
    # api = SmsSendAPIDemo(SECRET_ID, SECRET_KEY, BUSINESS_ID)
    # params = {
    #     "mobile": phone,
    #     "templateId": "10084",
    #     "paramType": "json",
    #     "params": "json格式字符串"
    # }
    # ret = api.send(params)
    # print(ret)

    return '123456'


# 用户中心
@user_bp.route('/center')
def user_center():
    print('----->', g.user.__dict__)
    types = Article_type.query.all()
    print('types=', types)
    photos=Photo.query.filter(Photo.user_id==g.user.id).all()
    return render_template('user/center.html', user=g.user, types=types,photos=photos)


# 图片的扩展名
ALLOWED_EXTENSIONS = ['jpg', 'png', 'gif', 'bmp']
# 用户信息修改


@user_bp.route('/change', methods=['GET', 'POST'])
def user_change():
    if request.method == 'POST':
        username = request.form.get('username')
        phone = request.form.get('phone')
        email = request.form.get('email')
        # 只要有图片，获取方式必须使用request.files.get(name)
        icon = request.files.get('icon')
        print('icon的值为：', icon)    # FileStorage
        # 属性：filename 用户获取文件的名字
        # 方法：save(保存路径)
        icon_name = icon.filename
        suffix = icon_name.rsplit('.')[-1]
        if suffix in ALLOWED_EXTENSIONS:
            print('----icon_name:', icon_name)
            # icon_name=secure_filename(icon_name)  # 保证文件名是符合python的命名规则
            print('----icon_name是:', icon_name)
            # file_path=os.path.join(Config.UPLOAD_ICON_DIR,icon_name)
            file_path = PurePath(Config.UPLOAD_ICON_DIR).joinpath(icon_name)
            icon.save(file_path)
            # 保存成功
            user = g.user
            user.username = username
            user.phone = phone
            user.email = email
            path = 'upload/icon'
            # user.icon=os.path.join(path,icon_name)
            user.icon = PurePosixPath(path).joinpath(icon_name)
            print('----icon_name是:', user.icon)

            print('----->user对象是：', user.__dict__)
            db.session.commit()
            return redirect(url_for('user.user_center'))
        else:
            return render_template('user/center.html', user=g.user, msg='扩展名必须是：jpg、png,gif,bpm格式')

        # # 查询一下手机号码
        # users = User.query.all()
        # for user in users:
        #     if user.phone == phone:
        #         # 说明数据库中已经有人注册此号码
        #         return render_template('user/center.html', user=g.user, msg='此号码已被注册')
    print('----->', g.user)
    return render_template('user/center.html', user=g.user)


# 发表文章
@user_bp.route('/article', methods=['GET', 'POST'])
def publish_article():
    if request.method == 'POST':
        title = request.form.get('title')
        type = request.form.get('type')
        content = request.form.get('content')
        print(content)
        return render_template('article/test.html', content=content)
    return '发表失败'


# 上传照片
@user_bp.route('/upload_photo', methods=['GET', 'POST'])
def upload_photo():
    # 获取上传的内容
    photo = request.files.get('photo')
    # 工具模块中封装方法
    ret, info = upload_qiniu_photo(photo)
    if info.status_code == 200:
        photo = Photo()
        photo.photo_name = ret['key']
        photo.user_id = g.user.id
        db.session.add(photo)
        db.session.commit()
        return redirect(url_for('user.user_center'))
    else:
        return '上传失败'


# 我的相册
@user_bp.route('/myphoto')
def myphoto():
    # 如果不转成整型，默认是str类型
    page=int(request.args.get('page',1))
    # 分页展示
    photos=Photo.query.paginate(page=page,per_page=5)
    user_id=session.get('uid',None)
    user=None
    if user_id:
        user=User.query.get(user_id)
    return render_template('user/myphoto.html',photos=photos,user=user)


# 删除相册图片
@user_bp.route('/photo_delete')
def photo_delete():
    pid=request.args.get('pid')
    photo=Photo.query.get(pid)
    filename=photo.photo_name
    # 封装好的一个删除七牛存储文件的函数
    info=delete_qiniu(filename)
    if info.status_code==200:
        # 删除数据库内容
        db.session.delete(photo)
        db.session.commit()
        return redirect(url_for('user.user_center'))
    else:
        return render_template('500.html',err_msg='删除相册图片失败！')
    
    
# aboutme 关于用户介绍添加
@user_bp.route('/about_me',methods=['POST'])  
def about_me():
    content=request.form.get('about')
    # 添加信息
    try:
        aboutme=AboutMe()
        aboutme.content=content
        aboutme.user_id=g.user.id
        db.session.add(aboutme)
        db.session.commit()
    except Exception as err:
        print('about更新错误：',err)
        return render_template('user/aboutme.html',user=g.user)
    else:
        return render_template('user/aboutme.html',user=g.user)


# 展示关于我
@user_bp.route('/showabout')    
def show_about():
    return render_template('user/aboutme.html',user=g.user)


# 留言板
@user_bp.route('/board',methods=['GET','POST'])
def show_board():
    # 获取登录用户信息
    uid=session.get('uid',None)
    user=None
    if uid:
        user=User.query.get(uid)
    # 查询所有的留言内容
    page=int(request.args.get('page',1))
    boards=MessageBoard.query.order_by(-MessageBoard.mdatetime).paginate(page=page,per_page=5)
    # 判断请求方式
    if request.method=='POST':
        content=request.form.get('board')
        print('content是:',content)
        # 添加留言
        msg_board=MessageBoard()
        msg_board.content=content
        if uid:
            msg_board.user_id=uid
        db.session.add(msg_board)
        db.session.commit()
        return redirect(url_for('user.show_board'))
    return render_template('user/board.html',user=user,boards=boards)
    
       
 # 删除留言
@user_bp.route('/board_del')
def delete_board():
    bid=request.args.get('bid')
    if bid:
        msgboard=MessageBoard.query.get(bid)
        db.session.delete(msgboard)
        db.session.commit()
        return redirect(url_for('user.user_center'))




# 删除失败500页面
@user_bp.route('/error')
def test_error():
    referer=request.headers.get('Referer',None)
    return render_template('500.html',err_msg='删除出现错误啦！',referer=referer)
    
    
    
# 退出
@user_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    # 1.cookie的方式
    response = redirect(url_for('user.index'))
    # 通过response对象的delete_cookie(key),key就是删除的cookie的key
    response.delete_cookie('uid')
    # 2.session的方式
    # del session['uid']
    session.clear()
    return response
