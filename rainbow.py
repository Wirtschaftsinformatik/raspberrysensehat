#!/bin/python3

from sense_hat import SenseHat
from instream import InStream
import time, json

sense = SenseHat()
sense.clear()

R=[255, 0, 0]
O=[255, 165, 0]
Y=[255, 255, 0]
G=[0, 128, 0]
B=[0, 0, 255]
I=[75, 0, 130]
V=[238, 130, 238]
X=[0, 0, 0]
W=[255, 255, 255]

rainbow = [
R, R, R, R, R, R, R, R,
R, O, O, O, O, O, O, O,
R, O, Y, Y, Y, Y, Y, Y,
R, O, Y, G, G, G, G, G,
R, O, Y, G, B, B, B, B,
R, O, Y, G, B, I, I, I,
R, O, Y, G, B, I, V, V,                                                                   
R, O, Y, G, B, I, V, X
]
sunny = [
Y, Y, Y, Y, Y, Y, Y, Y,
Y, Y, Y, Y, Y, Y, Y, Y,
Y, Y, Y, Y, Y, Y, Y, Y,
Y, Y, Y, Y, Y, Y, Y, Y,
Y, Y, Y, Y, Y, Y, Y, Y,
Y, Y, Y, Y, Y, Y, Y, Y,
Y, Y, Y, Y, Y, Y, Y, Y,
Y, Y, Y, Y, Y, Y, Y, Y
]
snow = [
W, W, W, W, W, W, W, W,
W, W, W, W, W, W, W, W,
W, W, W, W, W, W, W, W,
W, W, W, W, W, W, W, W,
W, W, W, W, W, W, W, W,
W, W, W, W, W, W, W, W,
W, W, W, W, W, W, W, W,
W, W, W, W, W, W, W, W
]

useSensor=True

while True:
	events=sense.stick.get_events()
	for event in events:
		if event.action=='pressed' and event.direction!='middle':
			if useSensor:
				print('Using data from openweathermap.org')
				stream=InStream('http://api.openweathermap.org/data/2.5/weather?q=Jena&units=metric&lang=de&APPID=7fa8d8270c50a5274bc055415e448b35')
				weather=json.loads(stream.readAll())['main']
			else:
				print('Using data from Raspberry Pi sensors')
			useSensor=not useSensor
	if useSensor:
		if sense.humidity>80 and sense.temp>20:
			sense.set_pixels(rainbow)
		elif sense.humidity<=80 and sense.temp>20:
			sense.set_pixels(sunny)
		elif sense.humidity>80 and sense.temp<0:
			sense.set_pixels(snow)
		else:
			sense.clear()
	else:
		if weather['humidity']>80 and weather['temp']>20:
			sense.set_pixels(rainbow)
		elif weather['humidity']<=80 and weather['temp']>20:
			sense.set_pixels(sunny)
		elif weather['humidity']>80 and weather['temp']<0:
			sense.set_pixels(snow)
		else:
			sense.clear()
	time.sleep(.5)
