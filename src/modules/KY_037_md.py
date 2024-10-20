import platform
import serial
import time
import threading
import pygame

# Handling the platform-specific serial port
SERIAL_PORT = "COM5" if platform.system() == "Windows" else "/dev/ttyUSB0"
BAUD_RATE = 9600

# Custom event types for jump and crouch
JUMP_EVENT = pygame.USEREVENT + 1
CROUCH_EVENT = pygame.USEREVENT + 2


def read_serial():
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
        time.sleep(2)  # Wait for the serial connection to establish
        print("Connected to the serial port")
        while True:
            line = ser.readline().decode("utf-8").strip()  # Read and decode the line
            if line:
                try:
                    # Parse the line as a float if it's a spike intensity
                    spike_intensity = float(line)
                    if spike_intensity > 10:
                        # Trigger the jump event
                        pygame.event.post(pygame.event.Event(JUMP_EVENT))
                    else:
                        # Trigger the crouch event
                        pygame.event.post(pygame.event.Event(CROUCH_EVENT))
                except ValueError:
                    # If parsing fails, ignore the line
                    pass
            time.sleep(0.1)


# Reading the serial must be done in a separate thread to prevent blocking
def start_serial_reader():
    serial_thread = threading.Thread(target=read_serial, daemon=True)
    serial_thread.start()
