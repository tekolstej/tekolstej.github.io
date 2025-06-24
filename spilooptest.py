import spidev

spi = spidev.SpiDev()
spi.open(0, 0)  # SPI Bus 0, Device 0
spi.max_speed_hz = 1000000

try:
    while True:
        response = spi.xfer2([0xAA])  # Send test byte
        print(f"Response: {response}")
except KeyboardInterrupt:
    spi.close()
