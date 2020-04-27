from picamera import PiCamera
import time

class Camera:
	def __init__(self, image_path):
		self.image_path = image_path
		
	def take_image(self):
	    print("Capturing image now...")
	    camera = PiCamera()
	    camera.start_preview()
	    time.sleep(2)
	    camera.capture(self.image_path)
	    camera.stop_preview()
