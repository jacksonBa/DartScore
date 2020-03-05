__author__ = 'teddycool'
# Alarm sound-types, no knowledge of actual alarm

import time
import RPi.GPIO as GPIO


class Buzzer(object):
    def __init__(self, GPIO, controlpin=5):
        print("Buzzer Init")
        self._gpio = GPIO
        # Grounded control pin = noise, control-pin pulled up...
        self._pin = controlpin
        self._gpio.setup(self._pin, self._gpio.OUT)
        self._gpio.setup(self._pin, 1)
        self._states = ['silent', 'test', 'hit']
        self._currentState = 'silent'
        self._lastStateChanged = time.time()

    def update(self):
        print("Current buzzerstate: " + self._currentState)
        if self._currentState == 'test':
            if time.time()-self._lastStateChanged > 2:
                self.set_state('silent')
        # Handle sound on/off etc for current state...
        return

    def stop(self):
        print("Buzzer silent")
        self._gpio.setup(self._pin, 1)
        return

    def start(self):
        print("Buzzer noisy")
        self._gpio.setup(self._pin, 0)
        return

    def set_state(self, state):
        if state in self._states:
            self._currentState = state
            self._lastStateChanged = time.time()
            if state == 'test':
                self.start()
            if state == 'silent':
                self.stop()
        else:
            print(state + " is not a valid buzzerstate")
        return

    def __del__(self):
        self.stop()
        print("Buzzer object deactivated and deleted for IO: " + str(self._pin))


if __name__ == '__main__':
    print("Testcode for Buzzer")

    GPIO.setmode(GPIO.BCM)

    buzzer = Buzzer(GPIO, 5)
    buzzer.start()
    time.sleep(2)
    buzzer.stop()
    GPIO.cleanup()
