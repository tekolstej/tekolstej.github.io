from gpiozero import Button
from time import sleep

# Define the GPIO pins for the sensors
float_sensor1 = Button(21, pull_up=True)  # Replace 17 with the actual GPIO pin
float_sensor2 = Button(1, pull_up=True)  # Replace 27 with the second GPIO pin

while True:
    if float_sensor1.is_pressed:
        print("Sensor 1 is triggered (float up)")
    else:
        print("Sensor 1 is not triggered (float down)")

    if float_sensor2.is_pressed:
        print("Sensor 2 is triggered (float up)")
    else:
        print("Sensor 2 is not triggered (float down)")

    sleep(1)

