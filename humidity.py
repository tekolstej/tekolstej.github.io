import time
import board
import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from adafruit_bme280 import advanced as adafruit_bme280

# Local CSV File
log_file = "datalog.csv"

# Set up Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("/home/jtk/Desktop/API Keys/infra-voyage-449419-q0-20615ec04069.json", scope)
client = gspread.authorize(creds)

# Open Google Sheet (Replace with your spreadsheet ID)
spreadsheet_id = "1djRyRE23ezG4-gMK-urluNUXNSs3IkXwOjtYdMAQjfo"  # Replace with your actual Google Sheets ID
sheet = client.open_by_key(spreadsheet_id).sheet1  # Opens the first sheet

# Add header to Google Sheet if empty
if not sheet.get_all_values():
    sheet.append_row(["Timestamp", "Temperature (°C)", "Pressure (hPa)", "Humidity (%)"])

# Set up BME280 sensor
i2c = board.I2C()  # Uses board.SCL and board.SDA
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)

# Optional: Set sea level pressure for altitude calculations
bme280.sea_level_pressure = 1013.25  # Adjust based on your local conditions

# Add a header to the CSV file if it does not exist
try:
    with open(log_file, "x", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Timestamp", "Temperature (°C)", "Pressure (hPa)", "Humidity (%)"])
except FileExistsError:
    pass  # File already exists; no need to add header

print(f"Logging data to {log_file} and Google Sheets every 60 seconds. Press Ctrl+C to stop.")

try:
    while True:
        # Get sensor readings
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        temperature = bme280.temperature
        pressure = bme280.pressure
        humidity = bme280.relative_humidity

        # Print data to the console
        print(f"{timestamp} - Temp: {temperature:.2f} °C, Pressure: {pressure:.2f} hPa, Humidity: {humidity:.2f} %")

        # Append data to local CSV file
        with open(log_file, "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([timestamp, temperature, pressure, humidity])

        # Append data to Google Sheet
        sheet.append_row([timestamp, temperature, pressure, humidity])

        # Wait 60 seconds before the next reading
        time.sleep(60)

except KeyboardInterrupt:
    print("\nDatalogging stopped.")
