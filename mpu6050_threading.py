from mpu6050_class import MPU6050

sensor = MPU6050()

def run_mpu6050():
    while True:
        sensor.update_gyro_data_deg()
        sensor.update_accel_data_g()

def get_gyro_data():
    gyro_x = sensor.gyro_x
    gyro_y = sensor.gyro_y
    gyro_z = sensor.gyro_z
    return gyro_x, gyro_y, gyro_z

def get_accl_data():
    accl_x = sensor.accl_x
    accl_y = sensor.accl_y
    accl_z = sensor.accl_z
    return accl_x, accl_y, accl_z
