from setuptools import find_packages, setup

setup(
	name='RasPyDHT',
	version='0.1dev',
	packages=find_packages(),
	install_requires=[
		'Adafruit-DHT', 
		'paho-mqtt',
		'smbus',
		],
)
