# Flask-Templates 模板

## Jinja2模板引擎

### 最简单的例子

index.py
```python
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    name = 'flask'
    return render_template('index.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)
```

templates/index.html
```html
<h2> Hello, {{ name }}!</h2>
```

Flask 提供的 render_template 函数把 Jinja2 模板引擎集成到了程序中。

render_template 函数的第一个参数是模板的文件名。
随后的参数都是键值对，表示模板中变量对应的真实值。

如上述代码中，左边的“name”表示参数名，就是模板中使用的占位符;右 边的“name”是当前作用域中的变量，表示同名参数的值。

### 模版中的变量

Jinja2 能识别所有类型的变量，甚至是一些复杂的类型，例如列表、字典和对象。在模板 中使用变量的一些示例如下:
```html
 <p>A value from a dictionary: {{ mydict['key'] }}.</p>
 <p>A value from a list: {{ mylist[3] }}.</p>
 <p>A value from a list, with a variable index: {{ mylist[myintvar] }}.</p>
 <p>A value from an object's method: {{ myobj.somemethod() }}.</p>
```

#### 使用过滤器修改变量
过滤器名添加在变量名之后，中间使用竖线分隔。
```html
 <p>Hello, {{ name|capitalize }}</p>
```

Jinja2变量过滤器:
    * safe          渲染值时不转义
    * capitalize    把值的首字母转换成大写,其他字母转换成小写
    * lower         把值转换成小写形式
    * upper         把值转换成大写形式
    * title         把值中每个单词的首字母都转换成大写
    *trim           把值的首尾空格去掉
    * striptags     渲染之前把值中所有的 HTML 标签都删掉

> safe 过滤器值得特别说明一下。默认情况下，出于安全考虑，Jinja2 会转义所有变量。例 如，如果一个变量的值为 '<h1>Hello</h1>'，Jinja2 会将其渲染成 '&lt;h1&gt;Hello&lt;/ h1&gt;'，浏览器能显示这个 h1 元素，但不会进行解释。很多情况下需要显示变量中存储 的 HTML 代码，这时就可使用 safe 过滤器。

#### 模版中的 控制结构

```html
{% if user %}
Hello, {{ user }}!
{% else %}
Hello, Stranger!
{% endif %}
```

```html
<ul>
{% for comment in comments %}
<li>{{ comment }}</li>
 {% endfor %}
</ul>
```

inja2 还支持宏。宏类似于 Python 代码中的函数。例如:
```html
{% macro render_comment(comment) %} <li>{{ comment }}</li>
{% endmacro %}
<ul>
{% for comment in comments %}
{{ render_comment(comment) }} {% endfor %}
</ul>
```
为了重复使用宏，将其保存在单独的文件中，然后导入:
```html
{% import 'macros.html' as macros %} <ul>
{% for comment in comments %}
{{ macros.render_comment(comment) }}
{% endfor %} </ul>
```

模版继承
创建一个名为 base.html 的基模板: 22 | 第3章
```html
<html>
     <head>
{% block head %}
<title>{% block title %}{% endblock %} - My Application</title> {% endblock %}
     </head>
     <body>
{% block body %}
{% endblock %} </body>
</html>
```
block 标签定义的元素可在衍生模板中修改。在本例中，我们定义了名为 head、title 和
body 的块。注意，title 包含在 head 中。

下面这个示例是基模板的衍生模板:
```html
{% extends "base.html" %}
{% block title %}Index{% endblock %} {% block head %}
         {{ super() }}
         <style>
         </style>
{% endblock %}
{% block body %} <h1>Hello, World!</h1> {% endblock %}
```

extends 指令声明这个模板衍生自 base.html。
在 extends 指令之后，基模板中的 3 个块被 重新定义，模板引擎会将其插入适当的位置。
注意新定义的 head 块，在基模板中其内容不 是空的，所以使用 super() 获取原来的内容。

### 自定义错误页面
```python
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
    
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
```
### 链接
任何具有多个路由的程序都需要可以连接不同页面的链接，例如导航条。

Flask 提供了 url_for() 辅助函数，它可以使用程序 URL 映射中保存 的信息生成 URL。
url_for() 函数最简单的用法是以视图函数名(或者 app.add_url_route() 定义路由时使用 的端点名)作为参数，返回对应的 URL。

1. url_for('index')得到的结果是/。调用url_for('index', _external=True)返回的则是绝对地址，在这个示例中是 http://localhost:5000/。
2. url_for ('user', name='john', _external=True) 的返回结果是 http://localhost:5000/user/john。
3. url_for('index', page=2) 的返回结果是 /?page=2。


### 静态文件

Web 程序不是仅由 Python 代码和模板组成, 还会使用静态文件，例如 HTML,img,css,js

默认设置下，Flask 在程序根目录中名为 static 的子目录中寻找静态文件。如果需要，可在 static 文件夹中使用子文件夹存放文件。
服务器收到前面那个 URL 后，会生成一个响应，包含文件系统中 static/css/styles.css 文件的内容。

比如favicon.ico 图标。
```
{% block head %}
{{ super() }}
<link rel="shortcut icon" href="{{ url_for('static', filename = 'favicon.ico') }}"
type="image/x-icon">
<link rel="icon" href="{{ url_for('static', filename = 'favicon.ico') }}"
type="image/x-icon"> {% endblock %}
```

图标的声明会插入 head 块的末尾。注意如何使用 super() 保留基模板中定义的块的原始 内容。     

