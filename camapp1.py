from flask import Flask, Response
import subprocess

app = Flask(__name__)

def generate_stream():
    """Stream video from Raspberry Pi camera."""
    command = [
        "libcamera-vid",
        "--camera", "0",
        "--width", "640",
        "--height", "480",
        "--codec", "mjpeg",
        "-o", "-",  # Output to stdout
        "-t", "0"   # Run indefinitely
    ]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=0)
    try:
        while True:
            frame = process.stdout.read(1024)
            if not frame:
                break
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    except GeneratorExit:
        process.terminate()
        process.wait()

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the img src attribute."""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    """Homepage with embedded video stream."""
    return '''
    <html>
        <head>
            <title>Raspberry Pi Camera Stream</title>
        </head>
        <body>
            <h1>Live Camera Stream</h1>
            <img src="/video_feed" width="640" height="480">
        </body>
    </html>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
