# coding=UTF-8
from flask import Flask, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room
import check
import sqldb

app = Flask(__name__)

socketio = SocketIO(app)

@app.route('/', methods=['GET'])
def home():
    return '<center style="margin-top:20px;"><h1>Home</h1></center>'

@app.route('/overdue', methods=['POST'])
def overdue():
    if check.check_session(request.form['session']):
        return 'ok'
    else:
        return 'no'

@app.route('/login', methods=['GET','POST'])
def login():
    return check.make_session(request.form['code'])

@socketio.on('join')
def handle_join(data):
    if check.check_session(data['session']):
        emit('join in', data, json = True)
        return
        
    emit('join in', 'session 过期', json = False)

if __name__ == '__main__':
    app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KTwf/,?KT'
    socketio.run(app, host='127.0.0.1', port = 8080)
