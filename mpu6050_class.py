# -*- coding: utf-8 -*-
"""
Created on Thu Apr  25 18:46:08 2019

@author: FujiiChang
"""
# slave address

import smbus

DEV_ADDR = 0x68         # device address
# register address
ACCEL_XOUT = 0x3b
ACCEL_YOUT = 0x3d
ACCEL_ZOUT = 0x3f
TEMP_OUT = 0x41
GYRO_XOUT = 0x43
GYRO_YOUT = 0x45
GYRO_ZOUT = 0x47
PWR_MGMT_1 = 0x6b       # PWR_MGMT_1
PWR_MGMT_2 = 0x6c       # PWR_MGMT_2

bus = smbus.SMBus(1)
# Sleep解除.
bus.write_byte_data(DEV_ADDR, PWR_MGMT_1, 0)

class MPU6050:
# ジャイロセンサ、加速度センサ関係==================================
    def __init__(self):
        self.gyro_x = 0
        self.gyro_y = 0
        self.gyro_z = 0
        self.accl_x = 0
        self.accl_y = 0
        self.accl_z = 0

    def read_byte(self, adr):
        return bus.read_byte_data(DEV_ADDR, adr)
    
    def read_word(self, adr):
        high = bus.read_byte_data(DEV_ADDR, adr)
        low = bus.read_byte_data(DEV_ADDR, adr+1)
        val = (high << 8) + low
        return val

        # Sensor data read
    def read_word_sensor(self, adr):
        val = self.read_word(adr)
        if (val >= 0x8000):         # minus
            return -((65535 - val) + 1)
        else:
            return val

    def get_gyro_data_lsb(self):
        x = self.read_word_sensor(GYRO_XOUT)
        y = self.read_word_sensor(GYRO_YOUT)
        z = self.read_word_sensor(GYRO_ZOUT)
        return x, y, z

    def update_gyro_data_deg(self):
        x, y, z = self.get_gyro_data_lsb()
        self.gyro_x = x / 131.0
        self.gyro_y = y / 131.0
        self.gyro_z = z / 131.0
        return self.gyro_x, self.gyro_y, self.gyro_z
    
    def get_accel_data_lsb(self):
        x = self.read_word_sensor(ACCEL_XOUT)
        y = self.read_word_sensor(ACCEL_YOUT)
        z = self.read_word_sensor(ACCEL_ZOUT)
        return x, y, z

    def update_accel_data_g(self):
        x, y, z = self.get_accel_data_lsb()
        self.accl_x = x / 16384.0
        self.accl_y = y / 16384.0
        self.accl_z = z / 16384.0
        return self.accl_x, self.accl_y, self.accl_z

    def get_temp(self):
        temp = self.read_word_sensor(TEMP_OUT)
        x = temp / 340 + 36.53      # data sheet(register map)記載の計算式.
        return x

