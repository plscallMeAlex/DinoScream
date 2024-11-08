signal = False
try:
    import RPi.GPIO as GPIO
    signal = True
except ImportError:
    print("RPi.GPIO not found. Using mock")
    signal = False


def check_button_press():
    if not signal:
        return False
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    if GPIO.input(19) == GPIO.LOW:
        GPIO.cleanup()
        return True
    return False
