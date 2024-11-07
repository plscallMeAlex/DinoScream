import platform
import serial
import time
import threading
import pygame

# Handling the platform-specific serial port
SERIAL_PORT = "COM5" if platform.system() == "Windows" else "/dev/ttyACM0"
BAUD_RATE = 9600

# Custom event types for jump and crouch
JUMP_EVENT = pygame.USEREVENT + 1
CROUCH_EVENT = pygame.USEREVENT + 2

# Cooldown
COOLDOWN = 1


def detected_module():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        ser.close()
        return True
    except serial.serialutil.SerialException:
        return False


def read_serial():
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
        time.sleep(1)  # Wait for the serial connection to establish
        print("Connected to the serial port")
        last_action_time = 0
        while True:
            line = ser.readline().decode("utf-8").strip()  # Read and decode the line
            if line:
                try:
                    # Parse the line as a float if it's a spike intensity
                    spike_intensity = float(line)
                    print("Intesity: ", spike_intensity)
                    current_time = time.time()
                    if current_time - last_action_time >= COOLDOWN:
                        if spike_intensity > 5:
                            # Trigger the jump event
                            pygame.event.post(pygame.event.Event(JUMP_EVENT))
                            last_action_time = current_time
                except ValueError:
                    # If parsing fails, ignore the line
                    pass
            time.sleep(0.1)


# Reading the serial must be done in a separate thread to prevent blocking
def start_serial_reader():
    # handle to use mock or read real serial
    if detected_module():
        serial_thread = threading.Thread(target=read_serial, daemon=True)
        serial_thread.start()
    else:
        print("Module not detected, using mock data.")
        pass
