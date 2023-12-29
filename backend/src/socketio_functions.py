from flask_socketio import SocketIO, send, emit

socketio = SocketIO()


def emit_to_socketio(event, data):
    socketio.emit(event, data)