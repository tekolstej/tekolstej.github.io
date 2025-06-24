import time
import csv
import lgpio
import board
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
    sheet.append_row([
        "Timestamp", "Temperature (°C)", "Pressure (hPa)", "Humidity (%)",
        "pH Voltage (V)", "pH Value", "TDS Voltage (V)", "TDS (ppm)", 
        "Float Sensor 1", "Float Sensor 2"
    ])

# Set up I2C for BME280 and ADS1115
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize BME280 sensor
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)
bme280.sea_level_pressure = 1013.25  # Adjust based on your local conditions

# Initialize ADS1115 for pH and TDS sensors
ads = ADS1115(i2c)
ph_channel = AnalogIn(ads, 0)  # Reading from A0 channel for pH
tds_channel = AnalogIn(ads, 1)  # Reading from A1 channel for TDS

# Set up GPIO for float sensors using lgpio
CHIP = 0  # GPIO chip
FLOAT1_PIN = 16  # GPIO 16
FLOAT2_PIN = 21  # GPIO 21

h = lgpio.gpiochip_open(CHIP)
lgpio.gpio_claim_input(h, FLOAT1_PIN)
lgpio.gpio_claim_input(h, FLOAT2_PIN)

# Calibration constants for TDS
TDS_FACTOR = 0.5  # Conversion factor (adjust based on your sensor)

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

# Function to convert ADC value to TDS
def adc_to_tds(voltage):
    """ Convert ADC voltage to TDS in ppm. """
    tds = voltage * TDS_FACTOR * 1000  # Convert voltage to ppm
    return tds

# Add a header to the CSV file if it does not exist
try:
    with open(log_file, "x", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            "Timestamp", "Temperature (°C)", "Pressure (hPa)", "Humidity (%)",
            "pH Voltage (V)", "pH Value", "TDS Voltage (V)", "TDS (ppm)", 
            "Float Sensor 1", "Float Sensor 2"
        ])
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

        # Read pH voltage and calculate pH
        ph_voltage = ph_channel.voltage
        pH_value = voltage_to_pH(ph_voltage)

        # Read TDS voltage and calculate TDS
        tds_voltage = tds_channel.voltage
        tds_value = adc_to_tds(tds_voltage)

        # Read float sensor statuses
        float1_status = "Water High" if lgpio.gpio_read(h, FLOAT1_PIN) == 0 else "Water Low"
        float2_status = "Water High" if lgpio.gpio_read(h, FLOAT2_PIN) == 0 else "No Water"

        # Print data to the console
        print(f"{timestamp} - Temp: {temperature:.2f} °C, Pressure: {pressure:.2f} hPa, "
              f"Humidity: {humidity:.2f} %, pH Voltage: {ph_voltage:.2f} V, pH: {pH_value:.2f}, "
              f"TDS Voltage: {tds_voltage:.2f} V, TDS: {tds_value:.2f} ppm, "
              f"High Float Sensor: {float1_status}, Float 2: {float2_status}")

        # Append data to local CSV file
        with open(log_file, "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([timestamp, temperature, pressure, humidity, ph_voltage, pH_value,
                             tds_voltage, tds_value, float1_status, float2_status])

        # Append data to Google Sheet
        sheet.append_row([timestamp, temperature, pressure, humidity, ph_voltage, pH_value,
                          tds_voltage, tds_value, float1_status, float2_status])

        # Wait 30 seconds before the next reading
        time.sleep(30)

except KeyboardInterrupt:
    lgpio.gpiochip_close(h)
    print("\nDatalogging stopped.")
