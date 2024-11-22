# from gpiozero import LightSensor, Buzzer
# import time

# ldr = LightSensor(4)  # alter if using a different pin
# while True:
#     print(ldr.value)
#     time.sleep(0.1)

# import RPi.GPIO as GPIO
# import time

# LDR_PIN = 4  # Replace with your GPIO pin number

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(LDR_PIN, GPIO.IN)

# try:
#     while True:
#         value = GPIO.input(LDR_PIN)
#         print(f"LDR Value: {value}")
#         time.sleep(0.5)
# except KeyboardInterrupt:
#     GPIO.cleanup()

from gpiozero import MCP3008

pot = MCP3008(0)

print(pot.value)
