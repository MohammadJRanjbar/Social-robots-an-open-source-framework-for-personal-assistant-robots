
from flask import Flask
from flask_socketio import SocketIO, emit, join_room, leave_room
#import cv2
#from deepface import DeepFace

app = Flask(__name__)

socketio = SocketIO(app, always_connect=True,cors_allowed_origins="*", engineio_logger=True)

@socketio.on('connect')
def connected():
    print('connect')
    
@socketio.on('disconnect')
def disconnect():
    print('disconnect')

@socketio.on('data')
def imageUpload(image):
    emit('send-image', image, broadcast = True)

if __name__ == '__main__':
    socketio.run(app,port=7000, debug=True)

