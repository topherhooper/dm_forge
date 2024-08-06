import socket
import cv2
import numpy as np
import struct
import threading
import pyaudio

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

    # Initialize audio
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

    def send_video():
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

    def send_audio():
        while True:
            data = stream.read(1024)
            conn.sendall(struct.pack("L", len(data)) + data)

    video_thread = threading.Thread(target=send_video)
    audio_thread = threading.Thread(target=send_audio)

    video_thread.start()
    audio_thread.start()

    video_thread.join()
    audio_thread.join()

    cap.release()
    stream.stop_stream()
    stream.close()
    audio.terminate()
    conn.close()
    server_socket.close()

    # Insert the HTML code for video chat
    html_code = '''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Video Chat</title>
</head>
<body>
<h1>Video Chat</h1>
<video id="video" autoplay></video>
<script src="//cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.0/socket.io.js"></script>
<script>
    const socket = io();

    socket.on('connect', () => {
        console.log('Connected to server');
    });

    socket.on('disconnect', () => {
        console.log('Disconnected from server');
    });
</script>
</body>
</html>
'''
    conn.sendall(html_code.encode())