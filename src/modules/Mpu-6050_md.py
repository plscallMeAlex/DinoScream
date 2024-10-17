import platform

# handle platform window can not controlling the MPU6050
is_windows = platform.system() == "Windows"

if not is_windows:
    from mpu6050 import mpu6050
else:

    class MockMPU6050:
        def get_accel_data(self):
            return {"x": 0.0, "y": 0.0, "z": 0.0}


def get_tilt_angle():
    sensor = mpu6050(0x68) if not is_windows else MockMPU6050()
    # handle the case where the sensor is not connected
    try:
        accel_data = sensor.get_accel_data()
        y = accel_data["y"]
        return y
    except Exception as e:
        print("Error reading from sensor: ", e)
        return None
