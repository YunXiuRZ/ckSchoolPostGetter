import sys
sys.path.append('function/')
from ckSchoolPostGetter import get_post
from ckSchoolPostPusher import send_messages

def start():
    get_post()
    send_messages()
    
if __name__ == '__main__':
    start()
