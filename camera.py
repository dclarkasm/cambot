from picamera import PiCamera
import time
from gpiozero import PWMLED
from time import sleep

class Camera:
    def __init__(self, image_path):
        self.image_path = image_path
        self.led = PWMLED(18)

    def sweep_led(self, direction):
        for b in range(100):
            c=b
            if direction == "OFF":
                c=100-b
            self.led.value = c / 100
            sleep(0.05)
    def take_image(self):
        print("Turning on LED...")
        self.sweep_led("ON")
        print("Capturing image now...")
        camera = PiCamera()
        camera.start_preview()
        time.sleep(2)
        camera.capture(self.image_path)
        camera.stop_preview()
        print("Turning off LED...")
        self.sweep_led("OFF")
