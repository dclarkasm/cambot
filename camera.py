from picamera import PiCamera
import time
from gpiozero import PWMLED
from time import sleep

class Camera:
    def __init__(self, image_path):
        self.image_path = image_path
        self.led_pin = 18
        self.led = None
        self.led_state = "OFF"

    def sweep_led(self, direction):
        if self.led_state == direction:
            return  # LED is already in desired state, return
        if self.led is None:
            self.led = PWMLED(self.led_pin)
            self.led.value = 0.0
        for b in range(100):
            c=b
            if direction == "OFF":
                c=100-b
            self.led.value = float(c) / 100.0
            sleep(0.05)
        self.led_state = direction
        if direction == "OFF":
            del self.led    # destroy LED obj to turn it off completely
            self.led = None

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

def timer_print(s):
    while s > 0:
        print(s)
        time.sleep(1)
        s = s-1

if __name__ == "__main__":
    print("Testing LED PWM sweep")
    c = Camera("test.jpg")
    print("Camera is initialized")
    #timer_print(5)
    print("LED is sweeping ON...")
    c.sweep_led("ON")
    print("LED is ON")
    while True:
        pass
    #timer_print(5)
    #print("LED is sweeping OFF...")
    #c.sweep_led("OFF")
    #print("LED is OFF")
    #timer_print(5)
    #del c
    #print("Called Camera destructor")
    #timer_print(5)
    #print("Exiting")
