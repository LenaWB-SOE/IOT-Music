from gpiozero import MotionSensor
import time

pir = MotionSensor(4, None, None, 4)

while True:
	# pir.wait_for_motion()
	# print("You moved")
	# pir.wait_for_no_motion()
    print(pir.value)
    time.sleep(0.01)