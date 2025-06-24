import time
import board
import busio
from adafruit_ads1x15.ads1115 import ADS1115
from adafruit_ads1x15.analog_in import AnalogIn

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize ADS1115
ads = ADS1115(i2c)
ads.gain = 1  # Set gain (1 = ±4.096V range)

# Use channel A0 for the TDS sensor
chan = AnalogIn(ads, 1)

# Calibration constants
TDS_FACTOR = 0.5  # Conversion factor (adjust based on your sensor)
TEMP_COEFFICIENT = 0.02  # Temperature compensation factor (20°C baseline)

# Function to convert ADC value to TDS
def adc_to_tds(adc_value, voltage_range=4.096):
    voltage = adc_value * voltage_range / 32767.0  # Convert to voltage
    tds = voltage * TDS_FACTOR * 1000  # Convert to ppm
    return tds

print("Starting TDS measurement...")
while True:
    # Read ADC value
    adc_value = chan.value
    tds_value = adc_to_tds(adc_value)
    
    # Print readings
    print(f"Raw ADC: {adc_value}, TDS (ppm): {tds_value:.2f}")
    time.sleep(1)
