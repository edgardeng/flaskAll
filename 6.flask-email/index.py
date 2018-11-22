from flask import Flask, render_template, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_mail import Mail, Message
from werkzeug.utils import redirect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config.from_pyfile('settings.py')

bootstrap = Bootstrap(app)
mail = Mail(app)


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
    # msg.body = render_template(template + '.txt', **kwargs)
    # msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)


if __name__ == '__main__':
    app.run(debug=True)
