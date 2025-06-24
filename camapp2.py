import subprocess
import time
from flask import Flask, Response

app = Flask(__name__)

def generate_frames():
    """Continuously stream frames from libcamera-vid via ffmpeg."""
    command = [
        "bash", "-c",  # Run the full pipeline inside bash
        "libcamera-vid --camera 0 --width 640 --height 480 --framerate 15 --codec mjpeg --output - | ffmpeg -i - -f mjpeg -"
    ]
    
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=0, shell=False)

    try:
        while True:
            frame = process.stdout.read(1024)  # Read frame chunk
            if not frame:
                break
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    finally:
        process.terminate()

@app.route('/video_feed')
def video_feed():
    """Serve the MJPEG stream."""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
