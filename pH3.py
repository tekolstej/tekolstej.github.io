import spidev
import time

# Initialize SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # SPI bus 0, CE0
spi.max_speed_hz = 1000000

# Define VREF for the ADC
VREF = 5.0  # Update if the ADC0834 is using a different reference voltage

def read_adc0834(channel):
    """Read from the ADC0834 (8-bit result)."""
    assert 0 <= channel <= 3, "Channel must be 0-3"
    cmd = [1, (8 + channel) << 4, 0]  # Command to start conversion
    adc = spi.xfer2(cmd)  # SPI transfer
    adc_value = adc[1]  # The ADC value is in the second byte
    return adc_value

try:
    while True:
        # Read pH signal from CH0
        adc_value_ph = read_adc0834(0)  # Read from CH0
        voltage_ph = adc_value_ph * (VREF / 255)  # Convert to voltage

        # Read temperature signal from CH1
        adc_value_temp = read_adc0834(1)  # Read from CH1
        voltage_temp = adc_value_temp * (VREF / 255)  # Convert to voltage

        print(f"Raw ADC (pH): {adc_value_ph}, Voltage (pH): {voltage_ph:.2f}V")
        print(f"Raw ADC (Temp): {adc_value_temp}, Voltage (Temp): {voltage_temp:.2f}V")
        time.sleep(1)
except KeyboardInterrupt:
    spi.close()
    print("Exiting...")
