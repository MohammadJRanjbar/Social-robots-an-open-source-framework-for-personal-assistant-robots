from flask import Flask
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)

socketio = SocketIO(app, always_connect=True, engineio_logger=True)

@socketio.on('connect')
def connected():
    print('connect')
    
@socketio.on('disconnect')
def disconnect():
    print('disconnect')

if __name__ == '__main__':
    socketio.run(app, host='45.149.77.212', port=5000,debug=True)
