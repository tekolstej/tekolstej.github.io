import time
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import requests

# Path to your service account JSON key file
KEY_FILE = "/home/jtk/KeysJSONs/ponicslogger.json"  # Replace * with your actual file name if needed

# URL endpoints on your dashboard
BME280_ENDPOINT = "http://localhost:5000/bme280_status"
PH_ENDPOINT = "http://localhost:5000/ph_status"
WATER_ENDPOINT = "http://localhost:5000/water_level_status"

# Google Sheet settings
SPREADSHEET_NAME = "Ponics Logger"

# Authenticate with Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file(KEY_FILE, scopes=scope)
client = gspread.authorize(creds)

# Open the sheet
sheet = client.open(SPREADSHEET_NAME).sheet1

def log_data():
    try:
        # Read sensor values from Flask endpoints
        bme_data = requests.get(BME280_ENDPOINT).json()
        ph_data = requests.get(PH_ENDPOINT).json()
        water_level = requests.get(WATER_ENDPOINT).text.strip()

        # Parse values
        temp_c = float(bme_data["temperature"])
        temp_f = round(temp_c * 9 / 5 + 32, 2)
        pressure = float(bme_data["pressure"])
        humidity = float(bme_data["humidity"])

        # Absolute Humidity (same calc as HTML dashboard)
        mw = 18.016
        r = 8314.3
        temp_k = temp_c + 273.15
        svp = 6.112 * (2.71828 ** ((17.67 * temp_c) / (temp_c + 243.5)))
        vp = svp * (humidity / 100)
        abs_humidity = round((1000 * mw * vp) / (r * temp_k), 2)

        ph = float(ph_data["pH"])
        voltage = float(ph_data["voltage"])

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Prepare row to insert
        row = [timestamp, temp_c, temp_f, pressure, humidity, abs_humidity, ph, voltage, water_level]

        # Append to sheet
        sheet.append_row(row)
        print(f"[Logged] {timestamp}")

    except Exception as e:
        print(f"[ERROR] Failed to log data: {e}")

if __name__ == "__main__":
    log_data()

