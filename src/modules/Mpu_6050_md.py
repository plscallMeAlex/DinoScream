import platform

# Global the sensor variable
sensor = None


# initialize the sensor by platform type
def init_sensor():
    global sensor
    is_windows = platform.system() == "Windows"
    if not is_windows:
        from mpu6050 import mpu6050

        sensor = mpu6050(0x68)
    else:
        # Mock the sensor for Windows Operating System
        class MockMPU6050:
            def get_accel_data(self):
                return {"x": 0.0, "y": 0.0, "z": 0.0}

        sensor = MockMPU6050()


# This function will return the tilt angle of the MPU6050 module
def get_tilt_angle():
    global sensor
    if sensor is None:
        init_sensor()

    # handle the case where the sensor is not connected
    try:
        accel_data = sensor.get_accel_data()
        y = accel_data["y"]  # use only y-axis data for moving the dino object
        return y
    except Exception as e:
        print("Error reading from sensor: ", e)
        return None
