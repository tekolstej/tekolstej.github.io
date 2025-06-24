from flask import Flask, Response, render_template, request, jsonify
import cv2
import threading

app = Flask(__name__)

camera = None  # Camera will be opened when needed
streaming = False  # Track whether streaming is active

def generate_frames():
    """Generator function to capture and stream frames."""
    global camera
    while streaming:
        if camera is None:
            break
        success, frame = camera.read()
        if not success:
            break
        else:
            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    """Render the main webpage."""
    return render_template('index.html', streaming=streaming)

@app.route('/start_stream', methods=['POST'])
def start_stream():
    """Start the camera stream."""
    global camera, streaming
    if not streaming:
        camera = cv2.VideoCapture(0)  # Open the camera
        streaming = True
        return jsonify({'status': 'started'})
    return jsonify({'status': 'already running'})

@app.route('/stop_stream', methods=['POST'])
def stop_stream():
    """Stop the camera stream."""
    global camera, streaming
    if streaming:
        streaming = False
        if camera is not None:
            camera.release()  # Release the camera
            camera = None
        return jsonify({'status': 'stopped'})
    return jsonify({'status': 'already stopped'})

@app.route('/video_feed')
def video_feed():
    """Stream video frames if streaming is active."""
    if streaming:
        return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    return Response("Stream is stopped.", mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
