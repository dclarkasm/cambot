from picamera import PiCamera

class Camera:
	def __init__(self, image_path):
		self.image_path = image_path
		
	def take_image():
	    print("Capturing image now...")
	    camera = PiCamera()
	    camera.start_preview()
	    sleep(2)
	    camera.capture(self.image_path)
	    camera.stop_preview()