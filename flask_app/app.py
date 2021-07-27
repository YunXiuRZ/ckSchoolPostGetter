# -*- coding: utf-8 -*
from flask import Flask
import sys
sys.path.append('../function')
from ckSchoolPostGetter import get_post
from ckSchoolPostPusher import send_messages

app = Flask(__name__)

@app.route('/get/')
def get():
    get_post()
    return 'get'

@app.route('/send/')
def send():
    send_messages()
    return 'send'

if __name__ == '__main__':
    app.debug = True
    app.run()
    