import time
import board
import busio
from adafruit_ads1x15.ads1115 import ADS1115
from adafruit_ads1x15.analog_in import AnalogIn

# Initialize I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize ADS1115
ads = ADS1115(i2c)

# Set up ADS1115 to read from A0
channel = AnalogIn(ads, 0)  # Attempting to read from channel 0

while True:
    print(f"Raw Value: {channel.value}, Voltage: {channel.voltage:.3f} V")
    time.sleep(1)

