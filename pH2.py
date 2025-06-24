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
chan = AnalogIn(ads, 0)

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

while True:
    # Read data from BME280
    temperature = bme280.temperature
    humidity = bme280.humidity
    pressure = bme280.pressure

    # Read data from pH probe (voltage)
    ph_voltage = chan.voltage
    pH_value = voltage_to_pH(ph_voltage)

    print(f"Temperature: {temperature:.2f} °C")
    print(f"Humidity: {humidity:.2f} %")
    print(f"Pressure: {pressure:.2f} hPa")
    print(f"pH Voltage: {ph_voltage:.2f} V")
    print(f"Calibrated pH: {pH_value:.2f}")
    time.sleep(1)
