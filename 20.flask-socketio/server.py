import random
import string

from flask import Flask, request, session, json, render_template
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from flask_socketio import Namespace
# from utils.redis_cli import Redis
# import shortuuid
from threading import Lock

users = {}
# 以下是Redis中的表结构  （key value 解释）
# 'users' SET(username) 根据‘users’ key查询多个在线用户名
# username SET(sid)  根据用户名key查询多个关联的socektio会话号，可能同一个用户在多个客户端进行socket.io连接
# sid STRING(username) 根据socketio会话号查询关联的用户名
class SocketServerNamespace(Namespace):
    lock = Lock()

    def on_connect(self):
        # flask请求中带有的socket.io会话号“sid”
        sid = request.sid
        print('connect, sid:{}'.format(sid))

    def on_disconnect(self):
        sid = request.sid
        # 从Redis中根据sid获取关联的在线用户名
        recorded_username = users.get(sid)
        # Redis事务
        if recorded_username:
            users.pop(sid)
                # 清除在线用户名和sid的关联记录
                # p.srem(recorded_username, sid)
                # # 清除该在线用户名记录
                # p.srem('users', recorded_username)
        else:
            print('sid:{} closed, but user is not online'.format(sid))
            # # 清除该sid记录
            # p.delete(sid)
            # # 执行该事务
            # p.execute()
        print('disconnect, sid:{}, username:{}, '.format(sid, recorded_username))


    # 处理来自socket.io客户端的“self_introduce”消息
    def on_self_introduce(self, data):
        print(data)
        username = data['from']
        sid = request.sid

        # username为空
        if not username:
            # 生成随机昵称
            username = ''.join(random.sample(string.ascii_letters + string.digits, 8))
            # 返回匿名随机昵称给客户端
            self.emit('anonymous_username', {'username': username}, sid)
        users[sid] = username
        # with Redis.r().pipeline() as p:
        #     # 增加该用户为在线用户
        #     p.sadd('users', username)
        #     # 增加一条username到sid的映射记录
        #     p.sadd(username, sid)
        #     # 设置sid对应的username
        #     p.set(sid, username)
        #     p.execute()
        print('self_introduced, sid:{}, username:{}'.format(sid, username))


    # 处理来自socket.io客户端的“list_users”消息
    def on_list_users(self, data):
        print(data)
        sid = request.sid
        user_from = data['from']
        # //获取在线用户列表
        user_ist = users.values() # list(Redis.r().smembers('users'))
        # //发送给请求的客户端
        self.emit('users_list', {'users_list': user_ist}, sid)
        print('received sid:{}, username:{}, list_users:{} '.format(sid, user_from, user_ist))

    # 处理来自socket.io客户端的“relay_msg_sig”消息
    def on_relay_msg_sig(self, data):
        print(data)
        user_from = data['from']
        user_to = data['to']
        msg = data['msg']
        sig = data['sig']
        timestamp = data['timestamp']
        # //查找目的客户端
        sids_to = users.get(user_to) # Redis.r().smembers(user_to)
        # //中转消息
        for sid in sids_to:
            self.emit('relay_msg_sig', data, sid)

    # def on_join(data):
    #     username = data['username']
    #     room = data['room']
    #     join_room(room)
    #     send(username + ' has entered the room.', room=room)
    #

    # def on_leave(data):
    #     username = data['username']
    #     room = data['room']
    #     leave_room(room)
    #     send(username + ' has left the room.', room=room)


# 封装socket.io服务
def socketio_server(app):
    # 将Flask的app实例封装进socketio实例
    socketio = SocketIO(app)
    # 配置socket.io的服务空间
    socketio.on_namespace(SocketServerNamespace('/socketio/'))

    # 配置默认错误处理函数
    @socketio.on_error_default
    def default_error_handler(e):

        print(request.event["message"])
        print(request.event["args"])

    return socketio


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('socketio_index.html', room='default')


if __name__ == '__main__':
    # 启动https服务
    socketio = socketio_server(app)
    socketio.run(app, '0.0.0.0',5003,  debug=True)
