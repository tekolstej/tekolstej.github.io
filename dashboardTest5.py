from flask import Flask, render_template, request, redirect, url_for, jsonify, Response
import RPi.GPIO as GPIO
import cv2
from picamera2 import Picamera2
import io
import board
import busio
from adafruit_bme280 import advanced as adafruit_bme280
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_ads1x15.ads1115 import ADS1115
import adafruit_ads1x15.ads1115 as ADS

app = Flask(__name__)

# Initialize camera
picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
picam2.start()

# I2C and Sensors
i2c = board.I2C()
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)
bme280.sea_level_pressure = 1013.25

ads = ADS.ADS1115(i2c)
ph_channel = AnalogIn(ads, ADS.P0)  # Assuming pH signal is on A0

# GPIO setup
RELAY_PIN = 15
PUMP_PIN = 18
SENSOR1_PIN = 17
SENSOR2_PIN = 14

GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(PUMP_PIN, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(SENSOR1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SENSOR2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def get_water_level():
    s1 = GPIO.input(SENSOR1_PIN)
    s2 = GPIO.input(SENSOR2_PIN)
    if s1 == GPIO.LOW and s2 == GPIO.LOW:
        return "HIGH"
    elif s1 == GPIO.HIGH and s2 == GPIO.HIGH:
        return "CRITICAL LOW"
    elif s1 == GPIO.HIGH and s2 == GPIO.LOW:
        return "MID"
    elif s1 == GPIO.LOW and s2 == GPIO.HIGH:
        return "ERROR"
    else:
        return "UNKNOWN"

def read_ph():
    voltage = ph_channel.voltage
    # Polynomial calibration
    pH = -0.334 * voltage**2 + 5.183 * voltage - 6.861
    return round(voltage, 3), round(pH, 2)

def generate_frames():
    while True:
        frame = picam2.capture_array()
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/")
def index():
    relay_state = GPIO.input(RELAY_PIN)
    pump_state = GPIO.input(PUMP_PIN)
    water_level = get_water_level()
    return render_template("index2test.html", light_on=relay_state == GPIO.LOW,
                           pump_on=pump_state == GPIO.LOW, water_level=water_level)

@app.route("/toggle", methods=["POST"])
def toggle():
    GPIO.output(RELAY_PIN, GPIO.LOW if GPIO.input(RELAY_PIN) == GPIO.HIGH else GPIO.HIGH)
    return redirect(url_for("index"))

@app.route("/pump_toggle", methods=["POST"])
def pump_toggle():
    GPIO.output(PUMP_PIN, GPIO.LOW if GPIO.input(PUMP_PIN) == GPIO.HIGH else GPIO.HIGH)
    return redirect(url_for("index"))

@app.route("/water_level_status")
def water_level_status():
    return get_water_level()

@app.route("/bme280_status")
def bme280_status():
    return jsonify({
        "temperature": round(bme280.temperature, 2),
        "pressure": round(bme280.pressure, 2),
        "humidity": round(bme280.relative_humidity, 2)
    })

@app.route("/ph_status")
def ph_status():
    voltage, ph = read_ph()
    return jsonify({"voltage": voltage, "pH": ph})

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=5000)
    finally:
        GPIO.cleanup()
