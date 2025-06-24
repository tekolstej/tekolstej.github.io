import lgpio
import time

# GPIO pin definitions for Pump 1
PUMP1_IN1 = 19
PUMP1_IN2 = 26

# GPIO pin definitions for Pump 2
PUMP2_IN1 = 9
PUMP2_IN2 = 11

# Initialize GPIO handles
h = lgpio.gpiochip_open(0)

# Set GPIO pins as outputs
lgpio.gpio_claim_output(h, PUMP1_IN1)
lgpio.gpio_claim_output(h, PUMP1_IN2)
lgpio.gpio_claim_output(h, PUMP2_IN1)
lgpio.gpio_claim_output(h, PUMP2_IN2)

# Functions to control Pump 1
def pump1_forward():
    lgpio.gpio_write(h, PUMP1_IN1, 1)
    lgpio.gpio_write(h, PUMP1_IN2, 0)

def pump1_backward():
    lgpio.gpio_write(h, PUMP1_IN1, 0)
    lgpio.gpio_write(h, PUMP1_IN2, 1)

def pump1_stop():
    lgpio.gpio_write(h, PUMP1_IN1, 0)
    lgpio.gpio_write(h, PUMP1_IN2, 0)

# Functions to control Pump 2
def pump2_forward():
    lgpio.gpio_write(h, PUMP2_IN1, 1)
    lgpio.gpio_write(h, PUMP2_IN2, 0)

def pump2_backward():
    lgpio.gpio_write(h, PUMP2_IN1, 0)
    lgpio.gpio_write(h, PUMP2_IN2, 1)

def pump2_stop():
    lgpio.gpio_write(h, PUMP2_IN1, 0)
    lgpio.gpio_write(h, PUMP2_IN2, 0)

# Test both pumps
try:
    print("Starting Pump 1 forward...")
    pump1_forward()
    time.sleep(5)  # Run for 5 seconds
    print("Stopping Pump 1...")
    pump1_stop()

    print("Starting Pump 2 backward...")
    pump2_backward()
    time.sleep(5)  # Run for 5 seconds
    print("Stopping Pump 2...")
    pump2_stop()

except KeyboardInterrupt:
    print("Stopping both pumps...")
    pump1_stop()
    pump2_stop()

finally:
    # Cleanup
    lgpio.gpiochip_close(h)
    print("GPIO cleanup complete.")
