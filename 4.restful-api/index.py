from flask import Flask, render_template, request, jsonify, abort
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

users = [
    {
        'id': 1,
        'name': 'Mr Zhao',
        'email': 'zhao@qq.com'
    },
    {
        'id': 2,
        'name': 'Mr Qian',
        'email': 'qian@qq.com'
    },
    {
        'id': 3,
        'name': 'Mr Sun',
        'email': 'sun@qq.com'
    }
]

@app.route('/')
def index():
    return render_template('index.html', users=users)


@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify({'users': users})


@app.route('/api/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = list(filter(lambda t: t['id'] == user_id, users))
    if len(user) == 0:
        abort(404)
    return jsonify({'user': user[0]})


@app.route('/api/user', methods=['POST'])
def add_user():
    # print(request.json)
    if not request.json or not 'name' in request.json:
        abort(400)
    index = users[-1]['id'] + 1 if len(users) > 0 else 1
    user = {
        'id': index,
        'name': request.json['name'],
        'email': request.json.get('email', '')
    }
    users.append(user)
    return jsonify({'user': user}), 200


@app.route('/api/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = list(filter(lambda t: t['id'] == user_id, users))
    print(user)
    print(request.json)
    if len(user) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'name' not in request.json:
        abort(400)
    if 'email' not in request.json:
        abort(400)
    user[0]['name'] = request.json.get('name', user[0]['name'])
    user[0]['email'] = request.json.get('email', user[0]['email'])
    return jsonify({'user': user[0]})


@app.route('/api/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = list(filter(lambda t: t['id'] == user_id, users))
    if len(user) == 0:
        abort(404)
    users.remove(user[0])
    return jsonify({'result': True})


if __name__ == '__main__':
    app.run(debug=True)
