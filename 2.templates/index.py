from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    name = 'flask'
    return render_template('index.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error/500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
