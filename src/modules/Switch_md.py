import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def check_button_press():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    if GPIO.input(19) == GPIO.LOW:
        GPIO.cleanup()
        return True
    GPIO.cleanup()
    return False
