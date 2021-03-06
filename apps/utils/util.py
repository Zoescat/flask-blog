# -*- coding: utf-8 -*-
# flake8: noqa
import random

from flask import session
from apps.article.models import Article, Article_type
from apps.user.models import User
from qiniu import Auth, put_file, etag,put_data,BucketManager


def upload_qiniu_photo(filestorage):
    # 需要填写你的 Access Key 和 Secret Key
    access_key = 'RJv20PACIHreB2VYLvBUXNfiUkDeb6oitpq6kIIs'
    secret_key = 'LYE4BSVajRTMYlKIKe0AzieQazJgvZOdL7UthJCd'

    # 构建鉴权对象
    q = Auth(access_key, secret_key)

    # 要上传的空间
    bucket_name = 'zoe-blog'

    # 上传后保存的文件名
    # key = 'my_blog.png'
    filename = filestorage.filename
    ran = random.randint(1, 1000)
    suffix = filename.rsplit('.')[-1]
    key = filename.rsplit('.')[0]+'_'+str(ran)+'.'+suffix
    # 

    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)

    # 要上传文件的本地路径
    # localfile = './sync/bbb.jpg'
    # ret, info = put_file(token, key, localfile)
    ret, info = put_data(token, key, filestorage.read())
    print(info)
    return ret,info



# 删除七牛存储图片
def delete_qiniu(filename):
    # 需要填写你的 Access Key 和 Secret Key
    access_key = 'RJv20PACIHreB2VYLvBUXNfiUkDeb6oitpq6kIIs'
    secret_key = 'LYE4BSVajRTMYlKIKe0AzieQazJgvZOdL7UthJCd'

    # 构建鉴权对象
    q = Auth(access_key, secret_key)

    # 要上传的空间
    bucket_name = 'zoe-blog'
    # 初始化BucketManager
    bucket=BucketManager(q)
    # key就是要删除的文件名字
    key = filename
    ret,info=bucket.delete(bucket_name,key)
    return info


# 文章分类
def user_type():
    # 获取文章分类
    types=Article_type.query.all()
    # 登录用户
    user=None
    user_id=session.get('uid',None)
    if user_id:
        user=User.query.get(user_id)
    return user,types