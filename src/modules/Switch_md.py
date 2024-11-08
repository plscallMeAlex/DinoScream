import time
signal = False

db_time = 0.2
last_press_time = 0
try:
    import RPi.GPIO as GPIO
    signal = True
except ImportError:
    print("RPi.GPIO not found. Using mock")
    signal = False


def check_button_press():
    global last_press_time
    if not signal:
        return False
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    if GPIO.input(19) == GPIO.LOW:
        current = time.time()

        if current - last_press_time > db_time:
            last_press_time = current
            GPIO.cleanup()
            return True
    GPIO.cleanup()
    return False
