import time
import board
from adafruit_bme280 import advanced as adafruit_bme280
import csv

# Create I2C object
i2c = board.I2C()  # Uses board.SCL and board.SDA

# Initialize the BME280 sensor
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)

# Optional: Set sea level pressure for altitude calculations
bme280.sea_level_pressure = 1013.25  # Adjust based on your local conditions

# Create and open the CSV file for datalogging
log_file = "datalog.csv"

# Add a header to the CSV file if it does not exist
try:
    with open(log_file, "x", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Timestamp", "Temperature (°C)", "Pressure (hPa)", "Humidity (%)"])
except FileExistsError:
    pass  # File already exists; no need to add header

# Log data every 60 seconds
print(f"Logging data to {log_file} every 60 seconds. Press Ctrl+C to stop.")
try:
    while True:
        # Get sensor readings
        temperature = bme280.temperature
        pressure = bme280.pressure
        humidity = bme280.relative_humidity
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")  # Current date and time

        # Print data to the console
        print(f"{timestamp} - Temp: {temperature:.2f} °C, Pressure: {pressure:.2f} hPa, Humidity: {humidity:.2f} %")

        # Append data to the CSV file
        with open(log_file, "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([timestamp, temperature, pressure, humidity])

        # Wait 60 seconds before the next reading
        time.sleep(60)

except KeyboardInterrupt:
    print("\nDatalogging stopped.")
