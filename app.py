
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import threading
import cv2
import socket
import numpy as np
import struct

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

def video_chat_server():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8081))  # Use a different port for video chat
    server_socket.listen(1)

    print("Video chat server listening on port 8081")

    # Accept a connection
    conn, addr = server_socket.accept()
    print(f"Connection from {addr}")

    # Capture video from the webcam
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Encode the frame
        encoded, buffer = cv2.imencode('.jpg', frame)
        data = np.array(buffer)
        stringData = data.tobytes()

        # Send the size of the frame first
        conn.sendall(struct.pack("L", len(stringData)) + stringData)

    cap.release()
    conn.close()
    server_socket.close()

if __name__ == '__main__':
    # Start the video chat server in a separate thread
    video_chat_thread = threading.Thread(target=video_chat_server)
    video_chat_thread.start()

    # Run the Flask server
    socketio.run(app, host='0.0.0.0', port=8080)