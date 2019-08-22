# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 17:11:30 2019

@author: FujiiChang
"""

import signal
import time
import threading
import GPS_threading as gps
import mpu6050_threading as mpu
import matplotlib.pyplot as plt
from statistics import mean, variance
from threading import Timer

gpsthread = threading.Thread(target=gps.rungps, args=())
sensor_threrad = threading.Thread(target=mpu.run_mpu6050, args=())
gpsthread.daemon = True
sensor_threrad.daemon = True
# start GPS and 6axis-sensor thread
gpsthread.start()
sensor_threrad.start()

now1 = []
now2 = []
now3 = []
exetime1 = []
exetime2 = []
exetime3 = []

class RepeatedTimer(Timer):
    def __init__(self, interval, function, args=[], kwargs={}):
        Timer.__init__(self, interval, self.run, args, kwargs)
        self.thread = None
        self.function = function
        self.time = []

    def run(self):
        self.thread = Timer(self.interval, self.run)
        self.thread.start()
        self.function(*self.args, **self.kwargs)

    def cancel(self):
        if self.thread is not None:
            self.thread.cancel()
            self.thread.join()
            del self.thread

class Sensor():
    def __init__(self):
        self.gyro_x = 0.0
        self.gyro_y = 0.0
        self.gyro_z = 0.0        
        self.accl_x = 0.0
        self.accl_y = 0.0
        self.accl_z = 0.0

    def update_gyro_value(self, gx, gy, gz):
        self.gyro_x = gx
        self.gyro_y = gy
        self.gyro_z = gz
        
    def update_accl_value(self, ax, ay, az):
        self.accl_x = ax
        self.accl_y = ay
        self.accl_z = az

class Robot():
    def __init__(self):
        self.roll = 0.0
        self.pitch = 0.0
        self.yaw = 0.0     
        self.vx = 0.0
        self.vy = 0.0
        self.vz = 0.0

robot = Robot()
sensor = Sensor()
                        
def make_freq_hist(x, hist_range, bin_num, tittle):
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.hist(x, range=hist_range, bins=bin_num)
    ax.set_ylim(0, 1000)
    ax.set_title('execute time histgram')
    ax.set_xlabel('execute time')
    ax.set_ylabel('freq')
    plt.savefig(tittle)
    plt.clf()
    
def calculate_state():
    robot.roll = robot.roll + sensor.gyro_x
    robot.pitch = robot.pitch + sensor.gyro_y
    robot.yaw = robot.yaw + sensor.gyro_z
    robot.vx = robot.vx + sensor.accl_x
    robot.vy = robot.vy + sensor.accl_y
    robot.vz = robot.vz + sensor.accl_z
    # print("3:calc###################")
    now3.append(time.time())    

def get_gyro_data(arg1, args2):
    gyro_x, gyro_y, gyro_z = mpu.get_gyro_data()
    sensor.update_gyro_value(gyro_x, gyro_y, gyro_z)
    # print("1:gyro######")
    now1.append(time.time())

def get_accl_data():
    accl_x, accl_y, accl_z = mpu.get_accl_data()
    sensor.update_accl_value(accl_x, accl_y, accl_z)
    # print("2:accl############")
    now2.append(time.time())

def gyro_signal():
    signal.signal(signal.SIGALRM, get_gyro_data)
    signal.setitimer(signal.ITIMER_REAL, 1, 0.1)

def kill_signal_process(arg1, args2):
    pass

if __name__=='__main__':    
    print("start")
    gyro_signal()
    accl_thread = RepeatedTimer(0.085, get_accl_data)
    calc_thread = RepeatedTimer(0.98, calculate_state)
    accl_thread.start()
    calc_thread.start()
    time.sleep(5)
    accl_thread.cancel()
    calc_thread.cancel()
    signal.signal(signal.SIGALRM, kill_signal_process)
    signal.setitimer(signal.ITIMER_REAL, 1, 0.1)
    print("finish")
    
    for i in range(len(now1)-1):
        exetime1.append(now1[i+1]-now1[i])   
        
    for i in range(len(now2)-1):
        exetime2.append(now2[i+1]-now2[i]) 
        
    for i in range(len(now3)-1):
        exetime3.append(now3[i+1]-now3[i])
    
    make_freq_hist(exetime1, (0.09, 0.18), 20, "excecute_time_histgram_gyro.png")
    mean1 = mean(exetime1)
    var1 = variance(exetime1)
    
    make_freq_hist(exetime2, (0.09, 0.18), 20, "excecute_time_histgram_accl.png")
    mean2 = mean(exetime2)
    var2 = variance(exetime2)
    
    make_freq_hist(exetime3, (0.09, 0.18), 20, "excecute_time_histgram_calc.png")
    mean3 = mean(exetime3)
    var3 = variance(exetime3)
    
    print("gyro mean: ", mean1)
    print("gyro variance: ", var1)    
    print("accl mean: ", mean2)
    print("accl variance: ", var2) 
    print("calc mean: ", mean3)
    print("calc variance: ", var3)
    print("Done.")  
