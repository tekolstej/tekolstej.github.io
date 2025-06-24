import lgpio
import time

# GPIO Setup
CHIP = 0  # GPIO chip
FLOAT1_PIN = 16  # GPIO 16 (High sensor)
FLOAT2_PIN = 21  # GPIO 21 (Low sensor)
PUMP1_IN1 = 19  # GPIO 19 (Pump 1 forward)
PUMP1_IN2 = 26  # GPIO 26 (Pump 1 backward)
PUMP2_IN1 = 9  # GPIO 9 (Pump 2 forward)
PUMP2_IN2 = 11  # GPIO 11 (Pump 2 backward)

#Initialize GPIO chip
h = lgpio.gpiochip_open(CHIP)

# Claim inputs for float sensors
lgpio.gpio_claim_input(h, FLOAT1_PIN)
lgpio.gpio_claim_input(h, FLOAT2_PIN)

# Claim outputs for pumps
lgpio.gpio_claim_output(h, PUMP1_IN1)
lgpio.gpio_claim_output(h, PUMP1_IN2)
lgpio.gpio_claim_output(h, PUMP2_IN1)
lgpio.gpio_claim_output(h, PUMP2_IN2)

# Pump Control Functions
def pump1_on():
    lgpio.gpio_write(h, PUMP1_IN1, 1)
    lgpio.gpio_write(h, PUMP1_IN2, 0)  # Forward direction

def pump1_off():
    lgpio.gpio_write(h, PUMP1_IN1, 0)
    lgpio.gpio_write(h, PUMP1_IN2, 0)

def pump2_on():
    lgpio.gpio_write(h, PUMP2_IN1, 1)
    lgpio.gpio_write(h, PUMP2_IN2, 0)  # Forward direction

def pump2_off():
    lgpio.gpio_write(h, PUMP2_IN1, 0)
    lgpio.gpio_write(h, PUMP2_IN2, 0)

# Function to determine water level and control pumps
def determine_water_level():
    float1_status = lgpio.gpio_read(h, FLOAT1_PIN)  # 0 = triggered, 1 = not triggered
    float2_status = lgpio.gpio_read(h, FLOAT2_PIN)  # 0 = triggered, 1 = not triggered

    if float1_status == 0 and float2_status == 0:  # Both sensors triggered
        water_level = "Low"
        pump1_on()  # Pump 1 fills water
        pump2_off()  # Pump 2 is off
    elif float1_status == 1 and float2_status == 0:  # Only float2 triggered
        water_level = "Half"
        pump1_off()  # Both pumps off
        pump2_off()
    elif float1_status == 1 and float2_status == 1:  # Neither sensor triggered
        water_level = "High"
        pump1_off()  # Pump 1 off
        pump2_on()  # Pump 2 drains water
    else:
        water_level = "Unknown"
        pump1_off()
        pump2_off()

    return water_level, float1_status, float2_status

# Main Loop
try:
    while True:
        # Determine water level and act on pumps
        water_level, float1_status, float2_status = determine_water_level()
        
        # Print water level and sensor statuses
        print(f"Float 1: {'Triggered' if float1_status == 0 else 'Not Triggered'}, "
              f"Float 2: {'Triggered' if float2_status == 0 else 'Not Triggered'}, "
              f"Water Level: {water_level}")
        
        time.sleep(1)  # Poll every second

except KeyboardInterrupt:
    print("\nStopping program and turning off pumps...")
    pump1_off()
    pump2_off()
    lgpio.gpiochip_close(h)
    print("GPIO cleanup complete.")
