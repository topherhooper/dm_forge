
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('connect')
def handle_connect():
    print("Client connected")

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

@socketio.on('set_grid_size')
def handle_set_grid_size(data):
    emit('update_grid_size', data, broadcast=True)

@socketio.on('move_token')
def handle_move_token(data):
    emit('update_token_position', data, broadcast=True)

@app.route('/')
def game():
    return render_template('game.html')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080)
