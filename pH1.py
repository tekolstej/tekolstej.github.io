import time
import board
import busio
from adafruit_bme280 import basic as adafruit_bme280
from adafruit_ads1x15.ads1115 import ADS1115
from adafruit_ads1x15.analog_in import AnalogIn

# Initialize I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize BME280 (address 0x76 or 0x77)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)

# Initialize ADS1115 (address 0x48)
ads = ADS1115(i2c)

# Set up ADS1115 channel A0
chan = AnalogIn(ads, 0)  # Correct channel definition

while True:
    # Read data from BME280
    temperature = bme280.temperature
    humidity = bme280.humidity
    pressure = bme280.pressure

    # Read data from pH probe (voltage)
    ph_voltage = chan.voltage

    # Print all sensor values
    print(f"Temperature: {temperature:.2f} °C")
    print(f"Humidity: {humidity:.2f} %")
    print(f"Pressure: {pressure:.2f} hPa")
    print(f"pH Voltage: {ph_voltage:.2f} V")  # Fixed line
    time.sleep(1)
