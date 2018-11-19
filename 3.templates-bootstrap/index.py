from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    name = 'flask'
    return render_template('index.html', name=name)


@app.route('/signup', methods=['GET'])
def signup():
    name = 'flask'
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signupPost():
    username = request.form['username']
    password = request.form['password']
    if username == 'admin' and password == 'admin':
        return render_template('index.html', name=username)
    return render_template('signup.html', message='Bad username or password', username=username)


if __name__ == '__main__':
    app.run(debug=True)
