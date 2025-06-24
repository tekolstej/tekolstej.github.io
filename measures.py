import time
import board
import csv
import busio
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from adafruit_bme280 import advanced as adafruit_bme280
from adafruit_ads1x15.ads1115 import ADS1115
from adafruit_ads1x15.analog_in import AnalogIn

# Local CSV File
log_file = "datalog.csv"

# Set up Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    "/home/jtk/Desktop/API Keys/infra-voyage-449419-q0-20615ec04069.json"
)
client = gspread.authorize(creds)

# Open Google Sheet (Replace with your spreadsheet ID)
spreadsheet_id = "1djRyRE23ezG4-gMK-urluNUXNSs3IkXwOjtYdMAQjfo"  # Replace with actual Google Sheets ID
sheet = client.open_by_key(spreadsheet_id).sheet1  # Opens the first sheet

# Add header to Google Sheet if empty
if not sheet.get_all_values():
    sheet.append_row(["Timestamp", "Temperature (°C)", "Pressure (hPa)", "Humidity (%)", "pH Voltage (V)", "pH Value"])

# Set up I2C for BME280 and ADS1115
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize BME280 sensor
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)
bme280.sea_level_pressure = 1013.25  # Adjust based on your local conditions

# Initialize ADS1115 for pH sensor
ads = ADS1115(i2c)
chan = AnalogIn(ads, 0)  # Reading from A0 channel

# Function to convert voltage to pH
def voltage_to_pH(voltage):
    """ Convert voltage from pH sensor to pH value using segmented calibration. """
    if voltage >= 3.75:  # Neutral to alkaline region (pH 7+)
        m = -13.64
        b = 58.15
    else:  # Acidic to neutral region (pH < 7)
        m = 1.345
        b = 1.96
    
    return m * voltage + b

# Add a header to the CSV file if it does not exist
try:
    with open(log_file, "x", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Timestamp", "Temperature (°C)", "Pressure (hPa)", "Humidity (%)", "pH Voltage (V)", "pH Value"])
except FileExistsError:
    pass  # File already exists; no need to add header

print(f"Logging data to {log_file} and Google Sheets every 30 seconds. Press Ctrl+C to stop.")

try:
    while True:
        # Get sensor readings
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        temperature = bme280.temperature
        pressure = bme280.pressure
        humidity = bme280.relative_humidity

        # Read pH voltage
        ph_voltage = chan.voltage
        pH_value = voltage_to_pH(ph_voltage)

        # Print data to the console
        print(f"{timestamp} - Temp: {temperature:.2f} °C, Pressure: {pressure:.2f} hPa, Humidity: {humidity:.2f} %, pH Voltage: {ph_voltage:.2f} V, pH: {pH_value:.2f}")

        # Append data to local CSV file
        with open(log_file, "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([timestamp, temperature, pressure, humidity, ph_voltage, pH_value])

        # Append data to Google Sheet
        sheet.append_row([timestamp, temperature, pressure, humidity, ph_voltage, pH_value])

        # Wait 30 seconds before the next reading
        time.sleep(30)

except KeyboardInterrupt:
    print("\nDatalogging stopped.")
