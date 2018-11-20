from flask import Flask, render_template, request, jsonify, abort
from flask_bootstrap import Bootstrap
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config['SECRET_KEY']='edgardeng'
app.config['MONGODB_SETTINGS'] = {
    'db':   'school',
    'host': '127.0.0.1',
    'port': 27017
}

bootstrap = Bootstrap(app)
db = MongoEngine(app)


class Users(db.Document):
    # 字段
    name = db.StringField(max_length=16, required=True)
    email = db.StringField(max_length=32, required=True)
    # 结构
    def __str__(self):
        return "name:{} - email:{}".format(self.name, self.email)


@app.route('/')
def index():
    all_users = Users.objects().all()
    return render_template('index.html', users=all_users)

@app.route('/user', defaults={'user_id': None})
@app.route('/user/<user_id>')
def user(user_id):
    if (user_id) :
        user = Users.objects(id=user_id).first()
        return render_template('edit.html', user=user)
    else:
        return render_template('edit.html')


@app.route('/api/users', methods=['GET'])
def get_users():
    all_users = Users.objects().all()
    return jsonify({'users': all_users})


@app.route('/api/user/<user_id>', methods=['GET'])
def get_user(user_id):
    user = Users.objects(id=user_id).first()
    if not user:
        return jsonify({'msg': 'no user'})
    return jsonify({'user': user})


@app.route('/api/user', methods=['POST'])
def add_user():
    # print(request.json)
    if not request.json or not 'name' in request.json or not 'email' in request.json:
        abort(400)
    name = request.json['name']
    email = request.json['email']
    user = Users(name=name, email=email).save()
    return jsonify({'user': user}), 200


@app.route('/api/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    user = Users.objects(id=user_id).first()
    if not user:
        abort(404)
    if not request.json or not 'name' in request.json or not 'email' in request.json:
        abort(400)
    name = request.json['name']
    email = request.json['email']
    result = user.update(name=name, email=email)
    return jsonify({'user': result})


@app.route('/api/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = Users.objects(id=user_id).first()
    if not user:
        abort(404)
    result = user.delete()
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True)
