"""
app.py

This is the main application file for the Flask web application. It sets up the Flask app, 
configures SocketIO for real-time communication, and defines the routes and event handlers.
"""

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('connect')
def handle_connect():
    """
    Event handler for client connection.
    """
    print("Client connected")

@socketio.on('disconnect')
def handle_disconnect():
    """
    Event handler for client disconnection.
    """
    print("Client disconnected")

@socketio.on('set_grid_size')
def handle_set_grid_size(data):
    """
    Event handler for setting the grid size.
    Broadcasts the new grid size to all connected clients.
    
    Args:
        data (dict): Dictionary containing the grid size.
    """
    emit('update_grid_size', data, broadcast=True)

@socketio.on('move_token')
def handle_move_token(data):
    """
    Event handler for moving a token.
    Broadcasts the new token position to all connected clients.
    
    Args:
        data (dict): Dictionary containing the token name and its new position.
    """
    emit('update_token_position', data, broadcast=True)

@app.route('/')
def game():
    """
    Route for the main game page.
    Renders the game.html template.
    
    Returns:
        str: Rendered HTML template for the game page.
    """
    return render_template('game.html')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080)
