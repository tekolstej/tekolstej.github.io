import spidev
import time

# Initialize SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # Bus 0, Device 0 (CS0)
spi.max_speed_hz = 1000000  # 1 MHz

# Function to read ADC0834 channel
def read_adc0834(channel):
    assert 0 <= channel <= 3, "Channel must be 0-3"
    # Send start bit, single/diff bit, and channel select bits
    cmd = [1, (8 + channel) << 4, 0]
    adc = spi.xfer2(cmd)
    value = ((adc[1] & 3) << 8) + adc[2]  # Combine 10-bit result
    return value

try:
    while True:
        adc_value = read_adc0834(0)  # Read channel 0
        voltage = adc_value * (3.3 / 255)  # Convert to voltage (8-bit resolution)
        print(f"ADC Value: {adc_value}, Voltage: {voltage:.2f}V")
        time.sleep(1)
except KeyboardInterrupt:
    spi.close()
