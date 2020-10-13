from flask import Flask, render_template, request, jsonify, abort
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY']='edgardeng'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://test:123456@localhost:3306/test"
app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app) # 获取SQLAlchemy实例对象


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<Role %r>' % self.name


class Users(db.Model):

    __tablename__ = 't_user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @staticmethod
    def as_dict_list(l):
        return [m.as_dict() for m in l]

    def __repr__(self):
        return '<User %r>' % self.name


@app.route('/')
def index():
    all_users = Users.query.all()
    return render_template('index.html', users=all_users)

@app.route('/user', defaults={'user_id': None})
@app.route('/user/<user_id>')
def user(user_id):
    if (user_id) :
        user = Users.query.filter_by(id=user_id).first()  # 条件查询
        return render_template('login.html', user=user)
    else:
        return render_template('login.html')


@app.route('/api/users', methods=['GET'])
def get_users():
    all_users = Users.query.all()
    return jsonify({'users': Users.as_dict_list(all_users)})


@app.route('/api/user/<user_id>', methods=['GET'])
def get_user(user_id):
    user = Users.query.filter_by(id=user_id).first()  # 条件查询
    if not user:
        return jsonify({'msg': 'no user'})
    return jsonify({'user': user.as_dict()})


@app.route('/api/user', methods=['POST'])
def add_user():
    if not request.json or not 'name' in request.json or not 'email' in request.json:
        abort(400)
    name = request.json['name']
    email = request.json['email']
    one = Users(name=name, email=email)
    one.id = db.session.add(one)
    db.session.commit()
    return jsonify({'user': one.as_dict()}), 200


@app.route('/api/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    user = Users.query.filter_by(id=user_id).first()
    if not user:
        abort(404)
    if not request.json or not 'name' in request.json or not 'email' in request.json:
        abort(400)
    name = request.json['name']
    email = request.json['email']
    Users.query.filter_by(id=user_id).update({'name': name, 'email': email})
    # db.session.update({'name': name, 'email': email})
    # db.session.commit()
    return jsonify({'user': user.as_dict()})


@app.route('/api/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    ones = Users.query.filter_by(id=user_id)
    if not user:
        abort(404)
    ones.delete()
    return jsonify({'result': True})


if __name__ == '__main__':
    app.run(debug=True)
