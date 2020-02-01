#!/usr/bin/python

import sys
import time
import argparse
import Adafruit_DHT

# Parse command line parameters.

sensor_type = {'11': Adafruit_DHT.DHT11,
               '22': Adafruit_DHT.DHT22,
               '2302': Adafruit_DHT.AM2302}

def dataread(type, gpio):
    humidity, temperature = Adafruit_DHT.read_retry(type, gpio)

    if humidity is not None and temperature is not None:
        print('{0:0.1f},{1:0.1f}'.format(temperature, humidity))

def parseCommandLine():
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', default='22', help='dht sensor type (11, 22, or 2302)')
    parser.add_argument('--gpio', type=int, default=4, help='GPIO port number')
    parser.add_argument('--samples', type=int, default=1, help='number of samples to collect')
    parser.add_argument('--sleep', type=int, default=2, help='Delay (s) between two readings')
    return parser.parse_args()


if __name__ == "__main__":
    args = parseCommandLine()
    dht = sensor_type[args.type]

    #Perform the first read
    dataread(dht, args.gpio)

    #Performs other reads
    for i in range(1, args.samples):
        time.sleep(args.sleep)
        dataread(dht, args.gpio)

    sys.exit(1)
