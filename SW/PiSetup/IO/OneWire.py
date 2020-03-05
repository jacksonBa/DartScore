__author__ = 'teddycool'
# This file is part of the DartScore project created by Pär Sundbäck
# More at https://github.com/teddycool/DartScore

# Purpose of this file:
# Handles the 1w interface for temperature in the 'machine-room'

import time


class OneWire(object):
    def __init__(self, GPIO, inputpin=12, mtimeout=10):
        print("Init temp monitoring")
        self._gpio = GPIO
        self._inputpin = inputpin
        self._timeout = mtimeout
        self._lastmeasure = None
        self._lastmtime = 0

    def initialize(self):
        self._measure()

    # Read temp
    def update(self):
        if time.time() - self._lastmeasure > self._timeout:
            self._measure()
        return self._lastmeasure

    def _measure(self):
        # self._lastmeasure =
        self._lastmtime = time.time()


if __name__ == '__main__':
    print("Testcode for TempMonitoring")
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)

    tm = OneWire(GPIO, 12, 3)
    tm.initialize()
    while True:
        print(tm.update)
        time.sleep(1)
