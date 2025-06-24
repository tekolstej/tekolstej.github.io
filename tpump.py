import lgpio
import time

# GPIO Setup
CHIP = 0  # GPIO chip
FLOAT1_PIN = 16  # GPIO 16 (High sensor)
FLOAT2_PIN = 21  # GPIO 21 (Low sensor)
PUMP1_IN1 = 19  # GPIO 19 (Pump 1 forward - fill pump)
PUMP1_IN2 = 26  # GPIO 26 (Pump 1 backward - unused)
PUMP2_IN1 = 9  # GPIO 9 (Pump 2 forward - drain pump)
PUMP2_IN2 = 11  # GPIO 11 (Pump 2 backward - unused)


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

# Read float sensor states
def read_float_sensors():
    float1_status = lgpio.gpio_read(h, FLOAT1_PIN)  # 0 = triggered, 1 = not triggered
    float2_status = lgpio.gpio_read(h, FLOAT2_PIN)  # 0 = triggered, 1 = not triggered
    return float1_status, float2_status

# Determine water level
def determine_water_level(float1_status, float2_status):
    if float1_status == 0 and float2_status == 0:  # Both sensors triggered
        return "Low"
    elif float1_status == 1 and float2_status == 0:  # Only top sensor triggered
        return "Possible error"
    elif float1_status == 1 and float2_status == 1:  # Neither sensor triggered
        return "High"
    elif float1_status == 0 and float2_status == 1: # Only bottom sensor triggered
        return "Over Half"
    else:
        return "Unknown"

# Main Logic
def main():
    try:
        # Set intervals
        fill_start_time = time.time()
        fill_duration = 5 * 60  # 5 minutes in seconds

        while True:
            # Read float sensor statuses
            float1_status, float2_status = read_float_sensors()
            water_level = determine_water_level(float1_status, float2_status)

            # Fill the bucket if it's low
            if water_level == "Low":
                print("Water level is Low. Turning on Pump 1 to fill.")
                pump1_on()
            elif water_level == "High":
                print("Water level is High. Turning off Pump 1.")
                pump1_off()

            # Maintain water level between Half and High
            if water_level == "Half" or water_level == "High":
                if time.time() - fill_start_time >= fill_duration:
                    print("5 minutes elapsed with sufficient water level. Starting drain pump (Pump 2).")
                    while True:
                        float1_status, float2_status = read_float_sensors()
                        water_level = determine_water_level(float1_status, float2_status)

                        if water_level == "Low":
                            print("Water level is Low. Turning off Pump 2.")
                            pump2_off()
                            return  # Restart main logic after draining
                        else:
                            print("Draining water...")
                            pump2_on()
                            time.sleep(1)

            # Log status
            print(f"Float 1: {'Triggered' if float1_status == 0 else 'Not Triggered'}, "
                  f"Float 2: {'Triggered' if float2_status == 0 else 'Not Triggered'}, "
                  f"Water Level: {water_level}")
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nStopping program and turning off pumps...")
        pump1_off()
        pump2_off()
        lgpio.gpiochip_close(h)
        print("GPIO cleanup complete.")

# Run the program
if __name__ == "__main__":
    main()
