import smbus
import time

I2C_ADDRESS = 0x23  # Address detected from i2cdetect
bus = smbus.SMBus(1)  # Use I2C bus 1

def relay_on(channel):
    """
    Turns ON the relay at the given channel.
    Each relay corresponds to a bit, so we send a bitmask to turn it on.
    """
    bus.write_byte(I2C_ADDRESS, 1 << (channel - 1))

def relay_off(channel):
    """
    Turns OFF all relays.
    If the relay module supports setting individual relays off, 
    you might need to modify this function.
    """
    bus.write_byte(I2C_ADDRESS, 0x00)  # Turn all relays off

# Test turning ON Relay 1
relay_on(1)
print("Relay 1 turned ON")
time.sleep(5)  # Keep it ON for 5 seconds
relay_off(1)
print("Relay 1 turned OFF")
