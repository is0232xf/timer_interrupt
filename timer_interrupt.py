# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 20:13:24 2019

@author: FujiiChang
"""

import signal
import time
import threading
import GPS_threading as gps
import mpu6050_threading as sensor
import matplotlib.pyplot as plt
from statistics import mean, variance

gpsthread = threading.Thread(target=gps.rungps, args=())
sensor_threrad = threading.Thread(target=sensor.run_mpu6050, args=())
gpsthread.daemon = True
sensor_threrad.daemon = True
# start GPS and 6axis-sensor thread
gpsthread.start()
sensor_threrad.start()

now = []
exetime = []
 
def make_freq_hist(x, hist_range, bin_num, tittle):
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.hist(x, range=hist_range, bins=bin_num)
    ax.set_ylim(0, 500)
    ax.set_title('execute time histgram')
    ax.set_xlabel('execute time')
    ax.set_ylabel('freq')
    plt.savefig(tittle)
    plt.clf()

def get_gyro_data(arg1, args2):
    gyro_x, gyro_y, gyro_z = sensor.get_gyro_data()
    now.append(time.time())

def get_accl_data(arg1, args2):
    accl_x, accl_y, accl_z = sensor.get_accl_data()
    return accl_x, accl_y, accl_z

def gyro_signal():
    signal.signal(signal.SIGALRM, get_gyro_data)
    signal.setitimer(signal.ITIMER_REAL, 1, 0.1)

print("start")
gyro_signal()
time.sleep(100)
print("finish")

for i in range(len(now)-1):
    exetime.append(now[i+1]-now[i])

make_freq_hist(exetime, (0.1, 0.18), 20, "excecute_time_histgram_signal.png")
mean = mean(exetime)
var = variance(exetime)
print("mean: ", mean)
print("variance: ", var)
print("Done.")
