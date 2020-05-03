from gpiozero import LED
import time
from bypass_rx import ShutdownBypassClient

BYPASS = False

def toggle_done():
    done = LED(2)   # signal indicates that cambot is finished and about to shutdown
    print("Toggling done signal..")
    done.off()
    time.sleep(0.5)
    done.on()
    time.sleep(0.5)
    done.off()

def myexit():
    global BYPASS
    sb = None
    try:
        sb = ShutdownBypassClient()
        if not sb.isBypass() and not BYPASS:
            toggle_done()
            exit(0)  # Shutdown
        exit(1)  # Don't shutdown
    finally:
        if sb is not None:
            sb.close()
