#!/usr/bin/env python

# Reference
# https://learn.sparkfun.com/tutorials/graph-sensor-data-with-python-and-matplotlib/update-a-graph-in-real-time


import argparse
import logging
import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import Adafruit_DHT
import datetime as dt


fig = plt.figure()
tPlot = fig.add_subplot(2, 1, 1)
hPlot = fig.add_subplot(2, 1, 2)

class DataPlot():
    def __init__(self):
        self.tx = []
        self.ty = []
        self.hx = []
        self.hy = []
    
# This function is called periodically from FuncAnimation
def plot_update(i, dataPl):
    # Try to grab a sensor reading.  Use the read_retry method which will retry up
    # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
    humidity, temperature = Adafruit_DHT.read_retry(22, 4)

    # Un-comment the line below to convert the temperature to Fahrenheit.
    # temperature = temperature * 9/5.0 + 32

    # Note that sometimes you won't get a reading and
    # the results will be null (because Linux can't
    # guarantee the timing of calls to read the sensor).
    # If this happens try again!
    if humidity is not None and temperature is not None:
        print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
        # Add x and y to lists
        now = dt.datetime.now().strftime('%H:%M:%S')
        dataPl.tx.append(now)
       	dataPl.ty.append(temperature)

        dataPl.hx.append(now)
        dataPl.hy.append(humidity)

        # Limit x and y lists to 20 items
        dataPl.tx = dataPl.tx[-30:]
        dataPl.ty = dataPl.ty[-30:]
		
        dataPl.hx = dataPl.hx[-30:]
        dataPl.hy = dataPl.hy[-30:]

        # Draw x and y lists
        tPlot.clear()
        tPlot.plot(dataPl.tx, dataPl.ty)
		
        hPlot.clear()
        hPlot.plot(dataPl.hx, dataPl.hy)
    else:
        print('Failed to get reading. Try again!')

try:
    data = DataPlot()
    ani = animation.FuncAnimation(fig, plot_update, fargs=({data}), interval=1000)
    plt.show()

except KeyboardInterrupt:
    sys.stdout.write("\rComplete!            \n")


