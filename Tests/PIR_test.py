from gpiozero import MotionSensor
import time

pir = MotionSensor(4)

while True:
	pir.wait_for_motion()
	print("You moved")
	time.sleep(1)
	# pir.wait_for_no_motion()
    #print(pir.value)