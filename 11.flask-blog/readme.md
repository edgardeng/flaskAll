# Flask Blog

> Flask Web Program。

## 相关功能 / Function

### 简单的权限管理 / Permission Manage

#### 角色 / Role

* 匿名(ANONYMITY)： Only Read
* 用户(USER)：post,comment,follow
* 管理员(ADMINISTER)： 查看用户，分配角色，禁止文章 / all permission: check all user, distribute role, forbid article


####  用户 / User

* 登录/Login
* 注册/Register
* 关注某人/follow someone
* 查看关注/ someone's follower and following

### 内容管理 / Content Manage

####  文章 / Article

* 新增文章 / add an article
* 修改文章 / update an article
* 删除文章 / delete an article
* 查看所有的文章 / check all articles

####  评论 / Comment

* 新增评论 / add a comment
* 修改评论 / update a comment
* 删除评论 / delete a comment
* 查看文章的评论 / check an article's comments

### Restful Api

> 本例使用flask_httpauth中的HTTPTokenAuth / HTTPTokenAuth in flask-httpauth used in this example.

>Put `{ "Authorization": "Bearer ********** }` in http request heads 

#### 认证 / 

* API登录认证 / api login 

* 登录Token / get login token

## extension

* [flask-bootstrap](https://travis-ci.org/mbr/flask-bootstrap) packages [Bootstrap](http://getbootstrap.com)

* [flask-script](https://flask-script.readthedocs.io/en/latest/) support for writing external scripts

* [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/)

* [Flask-Login](https://flask-login.readthedocs.io/en/latest/) implement user authentication

* [Flask-HttpAuth](https://flask-httpauth.readthedocs.io/en/latest/) implement user authentication in you api


