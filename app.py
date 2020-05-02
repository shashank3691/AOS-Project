#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
from flask import Flask, render_template, request
app = Flask(__name__, static_url_path='/static')
GPIO.setmode(GPIO.BCM)
pins = {14: {'name': 'Garage Door', 'state': GPIO.LOW}}
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)


@app.route('/')
def main():
    for pin in pins:
        pins[pin]['state'] = GPIO.input(pin)
    templateData = {'pins': pins}
    return render_template('main.html', **templateData)


@app.route('/<changePin>/<action>', methods=['GET', 'POST'])
def action(changePin, action):
    changePin = int(changePin)
    deviceName = pins[changePin]['name']
    if action == 'open':
        GPIO.output(changePin, GPIO.HIGH)
    if action == 'close':
        GPIO.output(changePin, GPIO.LOW)
    for pin in pins:
        pins[pin]['state'] = GPIO.input(pin)
    templateData = {'pins': pins}
    return render_template('main.html', **templateData)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
GPIO.cleanup()
