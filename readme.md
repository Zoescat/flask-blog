
* 使用命令：
    * 必须先在app.py中导入模型：
    ```python
    from apps.user.models import User
    ```
    *  在终端使用命令：db
    ```shell
    > python app.py db init  # 数据迁移，产生一个文件夹：migrations,同一个项目只执行一次即可
    > python app.py db migrate  # 自动产生一个版本文件 versions,每执行一次就产生一个版本文件
    > python app.py db upgrade  # 升级，同步内容到数据库
    > python app.py db downgrade    # 降级，降到当前文本的上个版本文件
    ```

# 一、使用flask-bootstrap的步骤：
 1.安装
```shell
> pip install flask-bootstrap
```
 2.进行配置
```python
from flask-bootstrap import Bootstrap
bootstrap=Bootstrap()
```
3.初始化bootstrap
```python
bootstrap.init__app(app=app)
```



# 二、会话机制
## 1.cookie方式
（1）保存

```python
# 通过response对象保存
response=redirect(xxx)
response=render_template(xxx)
response=Response()
response=make_response(xxx)
response=jsonify(xxx)
# 通过对象调用方法
response.set_cookie(key,value,max_age)
```
（2）获取

```python
# 通过response对象获取
response.form.get()
response.args.get()
cookie也在request对象中
request.cookie.get(key)
```
(3)删除
```python
通过response对象删除，把浏览器中的cookie删除
response=redirect(xxx)
response=render_template(xxx)
response=Response()
response=make_response(xxx)
response=jsonify(xxx)
# 通过对象调用方法
response.set_cookie(key,value,max_age)
```

## 2.session方式
```python
session.clear()   # 删除session的内存空间和删除cookie
del session[key]  # 常用，只会删除session中的这个键值对，不会删除session空间和cookie
```