from flask import Flask, render_template, request, jsonify, abort
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileRequired, FileAllowed
from werkzeug.utils import redirect, secure_filename
from wtforms import StringField, FileField
from wtforms.validators import DataRequired
# from flask.ext.uploads import UploadSet, IMAGES

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY']='edgardeng'


class PhotoForm(FlaskForm):
    photo = FileField('photo', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])


class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])

@app.route('/')
def index():
    message = request.args.get('msg')
    return render_template('index.html', message=message)


@app.route('/submit', methods=('GET', 'POST'))
def submit():
    form = MyForm()
    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data
        if name != 'admin' or password != 'admin':
            return render_template('submit.html', form=form, message='error name or password')
        else:
            return redirect('/?msg=hello,admin')
    return render_template('submit.html', form=form)


@app.route('/upload', methods=('GET', 'POST'))
def upload():
    form = PhotoForm()
    filename = None
    if form.validate_on_submit():
        filename = secure_filename(form.photo.data.filename)
        form.photo.data.save('uploads/' + filename)
        filename = '上传成功-' + filename
    return render_template('upload.html', form=form, message=filename)


if __name__ == '__main__':
    app.run(debug=True)
