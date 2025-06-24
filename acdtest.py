import spidev
import time

# Initialize SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # SPI bus 0, CE0
spi.max_speed_hz = 1000000  # Set SPI clock speed

# Define VREF for the ADC
VREF = 5.0  # Voltage reference for ADC (connected to 5V)

def read_adc0834(channel):
    """Read from the ADC0834."""
    assert 0 <= channel <= 3, "Channel must be 0-3"
    cmd = [1, (8 + channel) << 4, 0]  # Command to read from the specified channel
    adc = spi.xfer2(cmd)  # SPI transfer
    adc_value = adc[1]  # The ADC value is in the second byte
    return adc_value

try:
    while True:
        # Read CH0 (connected to 3.3V)
        adc_value = read_adc0834(0)  # Read from CH0
        voltage = adc_value * (VREF / 255)  # Convert ADC value to voltage
        print(f"Raw ADC Value: {adc_value}, Voltage: {voltage:.2f}V")
        time.sleep(1)  # Wait for 1 second
except KeyboardInterrupt:
    spi.close()
    print("Exiting...")
