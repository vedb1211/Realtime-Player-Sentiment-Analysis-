from flask import Flask, render_template, request
from flask_socketio import SocketIO
import cv2
import base64
import numpy as np
import tensorflow as tf
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
socketio = SocketIO(app)

# Initialize the video path to None
video_path = None

@app.route('/')
def index():
    return render_template('index_ws.html')

@app.route('/upload', methods=['POST'])
def upload():
    global video_path
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        video_path = os.path.join("uploads", uploaded_file.filename)
        uploaded_file.save(video_path)
    return '', 204  # Return an empty response with a "No Content" status code

def stop():
    shutdown_server()
    return jsonify(status="Server stopped"), 200

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

def generate_frames():
    global video_path
    model101 = tf.keras.models.load_model('C:/Users/4qin/OneDrive/Desktop/codes/ML/Crowd_model101.h5')

    while True:
        if video_path is not None:
            cap = cv2.VideoCapture(video_path)
            while True:
                success, frame = cap.read()
                if not success:
                    break
                else:
            # Preprocess the frame
                    resized_frame = cv2.resize(frame, (150, 150))
                    normalized_frame = resized_frame / 255.0
                    reshaped_frame = np.reshape(normalized_frame, (1, 150, 150, 3))
                    
                    # Make prediction
                    prediction = model101.predict(reshaped_frame)
                    
                    # Convert prediction to label
                    if prediction >= 0.56:
                        label = 'Expression: Happy'
                    elif 0.3 < prediction < 0.56:
                        label = 'Expression: Neutral'
                    else:
                        label = 'Expression: Sad'
                    
                    # Annotate the frame with the prediction
                    cv2.putText(frame, label, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

                    ret, buffer = cv2.imencode('.jpg', frame)
                    frame = base64.b64encode(buffer).decode('utf-8')
                    socketio.emit('frame', frame)
            cap.release()
            video_path = None  # Reset the video path

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')  # Create an uploads directory if it doesn't exist
    socketio.start_background_task(generate_frames)
    socketio.run(app, host='0.0.0.0', port=5000)
