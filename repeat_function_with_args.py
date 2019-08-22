# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 13:14:55 2019

@author: FujiiChang
"""

import time
import threading
import GPS_threading as gps
import mpu6050_threading as sensor
import matplotlib.pyplot as plt
from threading import Timer
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
   
            
def get_gyro_data():
    now.append(time.time())
    gyro_x, gyro_y, gyro_z = sensor.get_gyro_data()

def get_accl_data():
    accl_x, accl_y, accl_z = sensor.get_accl_data()

if __name__=='__main__':    
    print("thread start")
    t1 = RepeatedTimer(0.085, get_gyro_data)
    t2 = RepeatedTimer(0.085, get_accl_data)
    t1.start()
    t2.start()
    time.sleep(100)
    t1.cancel()
    t2.cancel()
    print("thread finish")
    for i in range(len(now)-1):
        exetime.append(now[i+1]-now[i])
    make_freq_hist(exetime, (0.08, 0.16), 20, "excecute_time_histgram_wide.png")
    make_freq_hist(exetime, (0.08, 0.16), 50, "excecute_time_histgram_narrow.png")
    mean = mean(exetime)
    var = variance(exetime)
    print("mean: ", mean)
    print("variance: ", var)
    print("Done.")