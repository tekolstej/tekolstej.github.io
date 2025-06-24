import lgpio
import time

CHIP = 0  # Raspberry Pi GPIO chip
FLOAT1_PIN = 16  # GPIO 16 (BCM)
FLOAT2_PIN = 21  # GPIO 21 (BCM)

h = lgpio.gpiochip_open(CHIP)
lgpio.gpio_claim_input(h, FLOAT1_PIN)
lgpio.gpio_claim_input(h, FLOAT2_PIN)

try:
    while True:
        sensor1 = lgpio.gpio_read(h, FLOAT1_PIN)
        sensor2 = lgpio.gpio_read(h, FLOAT2_PIN)

        print(f"Float Sensor 1: {'Triggered' if sensor1 == 0 else 'Not Triggered'}")
        print(f"Float Sensor 2: {'Triggered' if sensor2 == 0 else 'Not Triggered'}")

        time.sleep(1)
except KeyboardInterrupt:
    lgpio.gpiochip_close(h)
