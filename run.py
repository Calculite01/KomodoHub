from app import app, socketio

if __name__ == '__main__':
    socketio.run(app, debug=False, allow_unsafe_werkzeug=True, port=2222)
