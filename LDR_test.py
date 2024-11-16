from gpiozero import LightSensor, Buzzer
import time

ldr = LightSensor(4)  # alter if using a different pin
while True:
    print(ldr.value)
    time.sleep(1)