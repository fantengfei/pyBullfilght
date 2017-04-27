# coding=UTF-8

from flask import Flask, session, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room

import urllib
import random
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/', methods=['GET'])
def home():
    return '<center style="margin-top:20px;"><h1>Home</h1></center>'

@app.route('/login', methods=['GET','POST'])
def login():
    # https://api.weixin.qq.com/sns/jscode2session?appid=APPID&secret=SECRET&js_code=JSCODE&grant_type=authorization_code
    # AppID: wxe2018d200c505930
    # appsecret: be695b45f2b697ab837bd992baa8f676
    if request.method != 'POST':
        return False

    url = 'https://api.weixin.qq.com/sns/jscode2session?appid=wxe2018d200c505930&secret=be695b45f2b697ab837bd992baa8f676&js_code=' + request.form['code'] + '&grant_type=authorization_code'
    result = urllib.urlopen(url)
    # data = result.read()
    # print data
    j = json.load(result)
    print j

    session_key = j['session_key']
    openid = j['openid']

    if session_key and openid:
        session[openid] = session_key
        return session[openid]
    else:
        return False

@socketio.on('join')
def handle_join(data):
    emit('join in', data)

if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port = 8080)
