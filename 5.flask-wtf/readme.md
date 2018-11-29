# Flask中的Form

## Flask-WTF

> [flask-wtf](https://github.com/lepture/flask-wtf) - Simple integration of Flask and WTForms, including CSRF, file upload and Recaptcha integration。[Docs](http://www.pythondoc.com/flask-wtf/)

### 创建和验证表单

from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired

class MyForm(Form):
    name = StringField('name', validators=[DataRequired()])
Note
从 0.9.0 版本开始，Flask-WTF 将不会从 wtforms 中导入任何的内容，用户必须自己从 wtforms 中导入字段。

另外，隐藏的 CSRF 令牌会被自动地创建。你可以在模板这样地渲染它:

<form method="POST" action="/">
    {{ form.csrf_token }}
    {{ form.name.label }} {{ form.name(size=20) }}
    <input type="submit" value="Go">
</form>
尽管如此，为了创建有效的 XHTML/HTML， Form 类有一个 hidden_tag 方法， 它在一个隐藏的 DIV 标签中渲染任何隐藏的字段，包括 CSRF 字段:

<form method="POST" action="/">
    {{ form.hidden_tag() }}
    {{ form.name.label }} {{ form.name(size=20) }}
    <input type="submit" value="Go">
</form>
验证表单
在你的视图处理程序中验证请求:

@app.route('/submit', methods=('GET', 'POST'))
def submit():
    form = MyForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('submit.html', form=form)
注意你不需要把 request.form 传给 Flask-WTF；Flask-WTF 会自动加载。便捷的方法 validate_on_submit 将会检查是否是一个 POST 请求并且请求是否有效。

安全表单
无需任何配置，Form 是一个带有 CSRF 保护的并且会话安全的表单。我们鼓励你什么都不做。

但是如果你想要禁用 CSRF 保护，你可以这样:

form = Form(csrf_enabled=False)
如果你想要全局禁用 CSRF 保护，你真的不应该这样做。但是你要坚持这样做的话，你可以在配置中这样写:

WTF_CSRF_ENABLED = False
为了生成 CSRF 令牌，你必须有一个密钥，这通常与你的 Flask 应用密钥一致。如果你想使用不同的密钥，可在配置中指定:

WTF_CSRF_SECRET_KEY = 'a random string'
文件上传
Flask-WTF 提供 FileField 来处理文件上传，它在表单提交后，自动从 flask.request.files 中抽取数据。FileField 的 data 属性是一个 Werkzeug FileStorage 实例。

例如:

from werkzeug import secure_filename
from flask_wtf.file import FileField

class PhotoForm(Form):
    photo = FileField('Your photo')

@app.route('/upload/', methods=('GET', 'POST'))
def upload():
    form = PhotoForm()
    if form.validate_on_submit():
        filename = secure_filename(form.photo.data.filename)
        form.photo.data.save('uploads/' + filename)
    else:
        filename = None
    return render_template('upload.html', form=form, filename=filename)
Note
记得把你的 HTML 表单的 enctype 设置成 multipart/form-data，既是:

<form action="/upload/" method="POST" enctype="multipart/form-data">
    ....
</form>
此外，Flask-WTF 支持文件上传的验证。提供了 FileRequired 和 FileAllowed。

FileAllowed 能够很好地和 Flask-Uploads 一起协同工作, 例如:

from flask.ext.uploads import UploadSet, IMAGES
from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed, FileRequired

images = UploadSet('images', IMAGES)

class UploadForm(Form):
    upload = FileField('image', validators=[
        FileRequired(),
        FileAllowed(images, 'Images only!')
    ])
也能在没有 Flask-Uploads 下挑大梁。这时候你需要向 FileAllowed 传入扩展名即可:

class UploadForm(Form):
    upload = FileField('image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
HTML5 控件
Note
自 wtforms 1.0.5 版本开始，wtforms 就内嵌了 HTML5 控件和字段。如果可能的话，你可以考虑从 wtforms 中导入它们。

我们将会在 0.9.3 版本后移除 html5 模块。

你可以从 wtforms 中导入一些 HTML5 控件:

from wtforms.fields.html5 import URLField
from wtforms.validators import url

class LinkForm(Form):
    url = URLField(validators=[url()])
验证码
Flask-WTF 通过 RecaptchaField 也提供对验证码的支持:

from flask_wtf import Form, RecaptchaField
from wtforms import TextField

class SignupForm(Form):
    username = TextField('Username')
    recaptcha = RecaptchaField()
这伴随着诸多配置，你需要逐一地配置它们。

RECAPTCHA_PUBLIC_KEY	必须 公钥
RECAPTCHA_PRIVATE_KEY	必须 私钥
RECAPTCHA_API_SERVER	可选 验证码 API 服务器
RECAPTCHA_PARAMETERS	可选 一个 JavaScript（api.js）参数的字典
RECAPTCHA_DATA_ATTRS	可选 一个数据属性项列表 https://developers.google.com/recaptcha/docs/display
RECAPTCHA_PARAMETERS 和 RECAPTCHA_DATA_ATTRS 的示例:

RECAPTCHA_PARAMETERS = {'hl': 'zh', 'render': 'explicit'}
RECAPTCHA_DATA_ATTRS = {'theme': 'dark'}
对于应用测试时，如果 app.testing 为 True ，考虑到方便测试，Recaptcha 字段总是有效的。

在模板中很容易添加 Recaptcha 字段:

<form action="/" method="post">
    {{ form.username }}
    {{ form.recaptcha }}
</form>
