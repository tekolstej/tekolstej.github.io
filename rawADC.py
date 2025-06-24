import spidev
import time

# Initialize SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # SPI bus 0, CE0
spi.max_speed_hz = 1000000

# VREF for the ADC (update if using a different reference voltage)
VREF = 5.0

def read_adc0834(channel):
    """Read from the ADC0834."""
    assert 0 <= channel <= 3, "Channel must be 0-3"
    cmd = [1, (8 + channel) << 4, 0]  # Command to start conversion on the channel
    adc = spi.xfer2(cmd)  # SPI transfer
    adc_value = ((adc[1] & 3) << 8) + adc[2]  # Combine 10-bit result
    return adc_value

try:
    while True:
        # Read raw ADC values
        adc_value_ph = read_adc0834(0)  # Read from CH0 (pH)
        adc_value_temp = read_adc0834(1)  # Read from CH1 (temperature)

        print(f"Raw ADC (pH): {adc_value_ph}, Raw ADC (Temp): {adc_value_temp}")
        time.sleep(1)
except KeyboardInterrupt:
    spi.close()
    print("Exiting...")
