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


# Initialize GPIO chip
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
    elif float1_status == 0 and float2_status == 1:  # Only bottom sensor triggered
        return "Over Half"
    else:
        return "Unknown"

# Main Logic
def main():
    try:
        while True:
            # Step 1: Fill the bucket until it is full (High)
            while True:
                float1_status, float2_status = read_float_sensors()
                water_level = determine_water_level(float1_status, float2_status)

                if water_level == "High":
                    print("Bucket is full. Stopping input pump.")
                    pump1_off()
                    break
                else:
                    print("Bucket not full. Filling...")
                    pump1_on()
                time.sleep(1)

            # Step 2: Start 30-second timer to maintain water level
            print("Starting 30-second timer to maintain water level.")
            start_time = time.time()
            while time.time() - start_time < 30:
                float1_status, float2_status = read_float_sensors()
                water_level = determine_water_level(float1_status, float2_status)

                if water_level == "Low":
                    print("Water level is low during timer. Turning on input pump.")
                    pump1_on()
                else:
                    print("Water level is sufficient. Turning off input pump.")
                    pump1_off()

                time.sleep(1)

            # Step 3: Drain the bucket until it is empty (Low)
            print("30 seconds elapsed. Starting output pump to drain bucket.")
            while True:
                float1_status, float2_status = read_float_sensors()
                water_level = determine_water_level(float1_status, float2_status)

                if water_level == "Low":
                    print("Bucket is empty. Stopping output pump.")
                    pump2_off()
                    break
                else:
                    print("Draining bucket...")
                    pump2_on()
                time.sleep(1)

 # Step 4: End the program after completing one cycle
        print("Cycle complete. Stopping all pumps and exiting.")
        pump1_off()
        pump2_off()
        lgpio.gpiochip_close(h)
        print("GPIO cleanup complete.")
        return  # Exit the program

    except KeyboardInterrupt:
        print("\nStopping program and turning off pumps...")
        pump1_off()
        pump2_off()
        lgpio.gpiochip_close(h)
        print("GPIO cleanup complete.")

# Run the program
if __name__ == "__main__":
    main()
