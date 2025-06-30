import time
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Your spreadsheet name and worksheet
sheet = client.open("Hydroponics Data Log").sheet1

# Function to get sensor data
def get_data():
    bme = requests.get("http://localhost:5000/bme280_status").json()
    ph = requests.get("http://localhost:5000/ph_status").json()
    water = requests.get("http://localhost:5000/water_level_status").text

    tempC = bme["temperature"]
    tempF = round(tempC * 9 / 5 + 32, 2)
    rh = bme["humidity"]
    pressure = bme["pressure"]

    # Absolute Humidity (g/m³)
    tempK = tempC + 273.15
    svp = 6.112 * 2.71828 ** ((17.67 * tempC) / (tempC + 243.5))
    vp = svp * (rh / 100)
    abs_humidity = round((1000 * 18.016 * vp) / (8314.3 * tempK), 2)

    return [datetime.now().isoformat(), water, tempC, tempF, pressure, rh, abs_humidity, ph["pH"], ph["voltage"]]

# Append header if needed
if len(sheet.get_all_records()) == 0:
    sheet.append_row(["Timestamp", "Water Level", "Temp (C)", "Temp (F)", "Pressure", "RH (%)", "AH (g/m³)", "pH", "Voltage (V)"])

# Append data
data = get_data()
sheet.append_row(data)
