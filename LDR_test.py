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

# from gpiozero import MCP3008
# import time

# pot = MCP3008(0)

# while True:
#     print(pot.value)
#     time.sleep(0.5)

import time
import board
import busio
from digitalio import DigitalInOut
from adafruit_mcp3xxx.mcp3008 import MCP3008
from adafruit_mcp3xxx.analog_in import AnalogIn
from gpiozero import MCP3008

# Set up SPI and MCP3008
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = DigitalInOut(board.D5)  # Chip select pin (GPIO8 in Wiring)
#mcp = MCP3008(spi, cs)

# Connect LDR to channel 0 (CH0)
#ldr = AnalogIn(mcp, MCP3008.P0)
adc = MCP3008(channel=0, device=0)
print(str(adc.value*3.3))
# ldr = AnalogIn(mcp, 0)
# value = ldr.read_adc(0)
# print(value)

print("Reading LDR values...")
try:
    while True:
        # Read the raw value and voltage
        raw_value = ldr.value  # 0-65535
        voltage = ldr.voltage  # Voltage corresponding to the raw value

        print(f"Raw Value: {raw_value}, Voltage: {voltage:.2f} V")
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting program.")

