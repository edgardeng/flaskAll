# Flask Email

## Flask-Mail
> Flask-Mail提供电子邮件支持。 pip 安装: `(venv) $ pip install flask-mail`

Flask-Mail 连接到简单邮件传输协议(Simple Mail Transfer Protocol，SMTP)服务器，并 把邮件交给这个服务器发送。

如果不进行配置，Flask-Mail 会连接 localhost 上的端口 25， 无需验证即可发送电子邮件。

### Flask-Mail SMTP服务器的配置
MAIL_SERVER     localhost   电子邮件服务器的主机名或 IP 地址
MAIL_PORT       25          电子邮件服务器的端口
MAIL_USE_TLS    False       启用传输层安全(Transport Layer Security，TLS)协议
MAIL_USE_SSL    False       启用安全套接层(Secure Sockets Layer，SSL)协议
MAIL_USERNAME   None        邮件账户的用户名
MAIL_PASSWORD   None        邮件账户的密码


### 配置 Flask-Mail 使用 Gmail
```python
import os
from flask.ext.mail import Mail 
# ...
app.config['MAIL_SERVER'] = 'smtp.googlemail.com' 
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME') 
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

# Flask-Mail 的初始化
mail = Mail(app) 
```

> 千万不要把账户密令直接写入脚本，特别是当你计划开源自己的作品时。

### 在Python shell中发送电子邮件
你可以打开一个 shell 会话，发送一封测试邮件，以检查配置是否正确:
```
(venv) $ python hello.py shell
>>> from flask.ext.mail import Message
>>> from hello import mail
>>> msg = Message('test subject', sender='you@example.com', ... recipients=['you@example.com'])
>>> msg.body = 'text body'
>>> msg.html = '<b>HTML</b> body'
>>> with app.app_context():
... mail.send(msg)
```

### 在程序发送电子邮件

```python
class NameForm(FlaskForm):
    name = StringField('Send To?', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        send_email(name, 'New User')
        return redirect('/')
    return render_template('index.html', form=form)


def send_email(to, subject):
    prefix = app.config['FLASK_MAIL_SUBJECT_PREFIX'] + ' ' + subject
    msg = Message(prefix, sender=app.config['FLASK_MAIL_SENDER'], recipients=[to])
    msg.body = "testing"
    msg.html = "<b>testing</b>"
    templates
    templates
    mail.send(msg)
```
                                

每次你在表单中填写新名字时，管理员 都会收到一封电子邮件。
### 异步发送电子邮件

> mail.send()函数在发送电子邮件时停滞了几秒钟，过程中浏览器就像无响应一样。
为了避免处理请求过程中不必要的延迟，把发送电子邮件的函数移到后台线程中。

```python
from threading import Thread
     def send_async_email(app, msg):
         with app.app_context():
             mail.send(msg)
    def send_email(to, subject, template, **kwargs):
        msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
            sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to]) 
        msg.body = render_template(template + '.txt', **kwargs)
        msg.html = render_template(template + '.html', **kwargs)
        thr = Thread(target=send_async_email, args=[app, msg])
        thr.start()
        return thr
```

很多 Flask 扩展都假设已经存在激活的程序上下文和请求上下文。
Flask-Mail 中的 send() 函数使用 current_app，因此必须激活程序上下文。

程序要发送大量电子邮件时，使 用专门发送电子邮件的作业要比给每封邮件都新建一个线程更合适。
