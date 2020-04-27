from gpiozero import LED
import time

def myexit(code):
	done = LED(2)   # signal indicates that cambot is finished and about to shutdown
	print("Toggling done signal..")
	done.on()
	time.sleep(0.5)
	done.off()
	exit(code)