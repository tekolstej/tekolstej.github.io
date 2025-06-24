import time
import board
from adafruit_bme280 import advanced as adafruit_bme280

# Create I2C object
i2c = board.I2C()  # Uses board.SCL and board.SDA

# Initialize the BME280 sensor
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)

# Optional: Set sea level pressure for altitude calculations
bme280.sea_level_pressure = 1013.25  # Adjust based on your local conditions

# Read and display measurements
while True:
    print(f"Temperature: {bme280.temperature:.2f} °C")
    print(f"Pressure: {bme280.pressure:.2f} hPa")
    print(f"Humidity: {bme280.relative_humidity:.2f} %")
    time.sleep(1)
