# -*- coding: utf-8 -*-
"""
    index
    ~~~~~~
    :copyright: (c) 2017 by Taffy.
"""

from flask import Flask, request
from flask_socketio import SocketIO
import json
import check
import sqldb
from play import PlayNamespace

app = Flask(__name__)

socket = SocketIO(app)

socket.on_namespace(PlayNamespace('/'))

@app.route('/', methods=['GET'])
def home():
    return '<center style="margin-top:20px;"><h1>Home</h1></center>'

@app.route('/valid', methods=['POST'])
def session_valid():
    if check.check_session(request.form):
        return 'ok'
    else:
        return 'no'

@app.route('/login', methods=['GET','POST'])
def login():
    return json.dumps(check.make_session(request.form['code']))

if __name__ == '__main__':
    app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KTwf/,?KT'
    socket.run(app, host='0.0.0.0', port = 8080)
    
