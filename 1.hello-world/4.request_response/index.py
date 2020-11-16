"""
Flask Request and Response
"""
from flask import Flask, request, jsonify, session, redirect, url_for, escape
import json

app = Flask(__name__)

"""
    请求相关
        # request.method
        # request.args
        # request.form
        # request.values
        # request.cookies
        # request.headers
        # request.path
        # request.full_path
        # request.script_root
        # request.url
        # request.base_url
        # request.url_root
        # request.host_url
        # request.host
        # request.files
            # obj = request.files['the_file_name']
            # obj.save('/var/www/uploads/' + secure_filename(f.filename))
"""

"""
        响应相关
        # return "字符串"
        # return jsonify({})
        # return render_template('html模板路径',**{})
        # return redirect('/index.html')

        # response = make_response(render_template('index.html'))
        # response是flask.wrappers.Response类型
        # response.delete_cookie('key')
        # response.set_cookie('key', 'value')
        # response.headers['X-Something'] = 'A value'
        # return response
"""


@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s , <a href="/logout">logout here</a>' % escape(session['username'])
    return 'You are not logged in, please <a href="/login">login </a>'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    app.run(debug=True)
