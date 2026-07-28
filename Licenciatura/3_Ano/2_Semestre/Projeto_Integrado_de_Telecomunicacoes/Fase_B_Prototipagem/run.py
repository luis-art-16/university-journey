from app import create_app
from flask_socketio import SocketIO

app = create_app()
socketio = SocketIO(app)  # Make sure this matches your __init__.py

if __name__ == '__main__':
    socketio.run(app, debug=True)  # Instead of app.run()