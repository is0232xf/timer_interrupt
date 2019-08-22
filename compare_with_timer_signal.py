# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 15:05:56 2019

@author: FujiiChang
"""

import signal
import time
import threading
import GPS_threading as gps
import mpu6050_threading as sensor
import matplotlib.pyplot as plt
from statistics import mean, variance
from threading import Timer

gpsthread = threading.Thread(target=gps.rungps, args=())
sensor_threrad = threading.Thread(target=sensor.run_mpu6050, args=())
gpsthread.daemon = True
sensor_threrad.daemon = True
# start GPS and 6axis-sensor thread
gpsthread.start()
sensor_threrad.start()

now1 = []
now2 = []
exetime1 = []
exetime2 = []

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
    ax.set_ylim(0, 1000)
    ax.set_title('execute time histgram')
    ax.set_xlabel('execute time')
    plt.savefig(tittle)
    plt.clf()

def get_gyro_data(arg1, args2):
    gyro_x, gyro_y, gyro_z = sensor.get_gyro_data()
    now1.append(time.time())

def get_accl_data():
    accl_x, accl_y, accl_z = sensor.get_accl_data()
    now2.append(time.time())

def gyro_signal():
    signal.signal(signal.SIGALRM, get_gyro_data)
    signal.setitimer(signal.ITIMER_REAL, 1, 0.1)

if __name__=='__main__':    
    print("start")
    gyro_signal()
    t = RepeatedTimer(0.1, get_accl_data)
    t.start()
    time.sleep(100)
    t.cancel()
    print("finish")
    
    for i in range(len(now1)-1):
        exetime1.append(now1[i+1]-now1[i])   
        
    for i in range(len(now2)-1):
        exetime2.append(now2[i+1]-now2[i])
    
    make_freq_hist(exetime1, (0.09, 0.18), 20, "excecute_time_histgram_signal.png")
    mean1 = mean(exetime1)
    var1 = variance(exetime1)
    
    make_freq_hist(exetime2, (0.09, 0.18), 20, "excecute_time_histgram_timer.png")
    mean2 = mean(exetime2)
    var2 = variance(exetime2)
    
    print("signal mean: ", mean1)
    print("signal variance: ", var1)    
    print("timer mean: ", mean2)
    print("timer variance: ", var2)
    print("Done.")
        
