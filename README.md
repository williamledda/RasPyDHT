# RasPyDHT
Temperature and humidity monitoring system based on RaspberryPi board.

## Key future

* Support for DHT 11/22/AM2302.
* Temperature and Humidity displayed on a LCD1602 (controlled with I2C).
* Possibility to publish data with MQTT (see MQTT section below).
* Both console application and simple GUI that plots temperature and humidity over time.

## Dependency

* Requires python 3 (3.5.3+). It should work also on earlier version of Python 3, but not tested.
* Adafruit Python DHT library to read data from DHT Sensor (https://github.com/adafruit/Adafruit_Python_DHT).
* Sunfounder SensorKit for RPi2 library to control LCD162 with I2C 
(https://github.com/sunfounder/SunFounder_SensorKit_for_RPi2).
* smbus.
* matplotlib.

## Hardware required

* Raspberry pi (it can be any type or format).
* DHT22/DHT11/AM2302 temperature and humidity sensor. You can find many pre - assembled on an custom board, or you need 
to wire your self properly (very simple, you can find a lot of guides on how to do it).
* LCD1602 with I2C module (e.g. https://www.sunfounder.com/i2clcd.html). This simplify a lot the wiring and saves many 
I/O lines. You can also use a LCD1602 without the I2C module, but in this case you need to adjust the LCD1602.py python 
module to work properly.

## How to use

There are many ways you can use this package:

* Checkout this repository and run the script locally (see later).
* Installing the module.
* As system service.

## Installing module
To install, run `pip install raspydht` or checkout this repository and run `pip install .` from repository root folder
This installs into python allowing the scripts to executed from any path.

You can also install on a virtual environment (e.g. virtualenv) for testing it.

### Developer mode
If you want to be able to modify the code but still use from any location, you can checkout this repositorya amd 
install it in developer mode by running `pip install -e .`. 
This will install it but point to the files of this repository.

### Running locally
If you do not want to install, you can also checkout the repository and run the scripts from repository root. 
In this case you need to install the dependencies manually 

## Scripts
Thi package contains two applications that can be run as scripts

* ``rasdpydht``: is a console application that read data from the DHT sensor and display temperature and humidity 
on a LCD1602. Optionally it can also publish these data with MQTT protocol.
* ``raspydhtplot``: simple GUI application that plot temperature and DHT over time.

### raspydht

By installing the application (either with pip or from the local repository) you can run this application from any path
by simply typing ``raspydht``. If you have instead decide to do not install you can always run the application from the 
local repository as follow:

```shell script
$ cd <local repository root>
$ python3 -m raspydht 
```

or 

```shell script
$ cd <local repository root>
$ python3 runconsole.py  
```

Whatever option you choose, the following command line options are available:

```shell script 
  -h, --help       show this help message and exit
  --type TYPE      dht sensor type (11, 22, or 2302, default 22)
  --gpio GPIO      GPIO port number (default is 4)
  --sleep SLEEP    Delay (s) between two readings (default 2)
  --broker BROKER  MQTT broker host (default None)
  --verbose        Log info into console (default false)
  --room ROOM      Room name (default Room_1)
```

### raspydhtplot

By installing the application (either with pip or from the local repository) you can run this application from any path
by simply typing ``raspydhtplot``. If you have instead decide to do not install you can always run the application from the local repository as follow:

```shell script
$ cd <local repository root>
$ python3 -m raspydhtplot 
```

or 

```shell script
$ cd <local repository root>
$ python3 runplot.py  
```

Whatever option you choose, the following command line options are available:

```shell script 
  -h, --help     show this help message and exit
  --type TYPE    dht sensor type (11, 22, or 2302, default 22)
  --gpio GPIO    GPIO port number, default 4
  --sleep SLEEP  Delay (s) between two readings, default 2
  --verbose      Log info into console
```

Differently from the console application, there's no option to publish temperature 
and humidity as MQTT topics.

### Running as service

A service file can be created to run ``aspydht`` as daemon at boot. An example of service file is available in 
``service/raspydht.service`` of this repository and looks like the following:

```shell script
[Unit]
Description=RasPyDHT Service
Requires=systemd-modules-load.service
After=systemd-modules.load.service network.target network-online.target

[Service]
Type=simple
KillSignal=SIGINT
ExecStart=/usr/bin/python3 -m raspydht --broker <IP address of mqtt broker if any> --room <Room description>
SyslogIdentifier=RasPyDHT

[Install]
WantedBy=multi-user.target
```

You have to customize the ``ExecStart`` command to fit with your installation and with the options you prefer. 
You can also run from a virtual environment, e.g. with virtualenv:

```shell script
ExecStart=/home/pi/RasPyDHT-env/bin/python -m raspydht --verbose --broker localhost --room Room
```

Once you have customized service to fit your needs, you can install and enable it as follow:

``` shell script
$ sudo install -m 755 raspydht.service /etc/systemd/system
$ sudo systemctl daemon-reload
$ sudo systemctl enable raspydht.service
```

Doing this, ``raspydht`` will run automatically at boot. You can always start/stop/restart the service manually as follow:

``` shell script
$ sudo systemctl start srapydht
$ sudo systemctl stop raspydht
$ sudo systemctl restart raspydht
```

## MQTT topics

By running ``raspydht`` script with the ``--broker`` option, you will publish temperature and humidity as MQTT topics.
These topics have the following format:

``` 
RasPyDHT/<Room>/temperature xxx
RasPyDHT/<Room>/humidity xxx
``` 

Both topics are string. The room can configured using the ``--room`` script's option (default is "Room_1").