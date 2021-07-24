# -*- coding: utf-8 -*
from flask import Flask
from ckSchoolPostGetter import get_post
from ckSchoolPostPusher import send_messages

app = Flask(__name__)

@app.route('/get/')
def get():
    get_post()
    return 0

@app.route('/send/')
def send():
    send_messages()
    return 0

if __name__ == '__main__':
    app.debug = True
    app.run()
    