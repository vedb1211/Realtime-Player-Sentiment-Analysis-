# Realtime-Player-Sentiment-Analysis-


This project involves real-time sentiment analysis of players' expressions in a cricket match using a Convolutional Neural Network (CNN). The system captures video frames, preprocesses them, and analyzes the facial expressions of players to determine their sentiments. The sentiment predictions (Happy, Neutral, or Sad) are then displayed on the video frames in real-time.


https://github.com/vedb1211/Realtime-Player-Sentiment-Analysis-/assets/106091820/1dfebd10-3f06-4b26-aef6-c274046ea417


## Project Structure

- **index_ws.html:** HTML file containing the user interface for the real-time video display and file upload functionality.

- **app.py:** Python script that defines the Flask web application and handles video upload, sentiment analysis, and real-time communication using Socket.IO.

- **Crowd_model101.h5:** Pre-trained CNN model for sentiment analysis. The model predicts player sentiments based on facial expressions.

## How to Run the Project

1. Install the required Python packages:
   ```bash
   pip install flask flask_socketio opencv-python tensorflow

2. Run the Flask application:
   ```bash
   python app_websocket.py

   
