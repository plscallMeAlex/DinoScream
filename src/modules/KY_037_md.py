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
                        if spike_intensity > 9:
                            # Trigger the jump event
                            pygame.event.post(pygame.event.Event(JUMP_EVENT))
                            last_action_time = current_time
                        elif spike_intensity <= 9:
                            # Trigger the crouch event
                            pygame.event.post(pygame.event.Event(CROUCH_EVENT))
                            last_action_time = current_time
                except ValueError:
                    # If parsing fails, ignore the line
                    pass
            time.sleep(0.1)


# mock for windows testing without module
def read_mock_serial():
    last_action_time = 0
    while True:
        events = pygame.event.get()
        current_time = time.time()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if current_time - last_action_time >= COOLDOWN:
                    if (
                        event.key == pygame.K_UP
                    ):  # Simulate 'jump' on UP arrow key press
                        print("JUMP")
                        pygame.event.post(pygame.event.Event(JUMP_EVENT))
                        last_action_time = current_time
                    elif (
                        event.key == pygame.K_DOWN
                    ):  # Simulate 'crouch' on DOWN arrow key press
                        print("CROUCH")
                        pygame.event.post(pygame.event.Event(CROUCH_EVENT))
                        last_action_time = current_time

        time.sleep(0.1)


# Reading the serial must be done in a separate thread to prevent blocking
def start_serial_reader():
    # handle to use mock or read real serial
    target = read_serial if platform.system() != "Windows" else read_mock_serial

    serial_thread = threading.Thread(target=target, daemon=True)
    serial_thread.start()
