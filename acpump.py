import smbus
import time


I2C_ADDRESS = 0x23  # Address detected from i2cdetect. May have to chnage based on 'i2cdetect -y 1'
bus = smbus.SMBus(1)  # Use I2C bus 1


def relay_on(channel):
    bus.write_byte(I2C_ADDRESS, 1 << (channel - 1))

def relay_off(channel):
    bus.write_byte(I2C_ADDRESS, 0)

# Turn on Relay 1 (Pump)
relay_on(1)
time.sleep(5)  # Run pump for 5 seconds
relay_off(1)
