# coding=UTF-8

from flask import Flask
from flask import request
from flask import jsonify

users = {}

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return '<h1>Home</h1>'

@app.route('/list', methods=['GET'])
def list():
    return jsonify(users)

@app.route('/user', methods=['GET', 'POST'])
def user():
    u = (request.json)['user']
    k = u['avatarUrl']
    if k not in users:
        users[k] = u
        return 'success'
    else:
        return 'failure'

if __name__ == '__main__':
    app.run()