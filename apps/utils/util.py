# -*- coding: utf-8 -*-
# flake8: noqa
import random
from qiniu import Auth, put_file, etag,put_data
import qiniu.config


def upload_qiniu_photo(filestorage):
    # 需要填写你的 Access Key 和 Secret Key
    access_key = ''
    secret_key = ''

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
