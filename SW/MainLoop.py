__author__ = 'teddycool'

# DartScore MainLoop
# State-switching and handling of general rendering
# -> update -> draw....

import os
import sys
import time
import Cam
import RPi.GPIO as GPIO
from DartScoreEngine.DartScoreEngineConfig import dartconfig
from DartScoreEngine.StateLoops import PlayStateLoop
from DartScoreEngine.StateLoops import CamCalibrateLoop
from DartScoreEngine.StateLoops import CamMoutningLoop
from PiSetup.IO import ArcadeButton
sys.path.append("/home/pi/DartScore/SW")


class MainLoop(object):
    def __init__(self, camurl=dartconfig["cam"]["camurl"]):
        # TODO: fix logging to file readable from web
        self._cam = Cam.create_cam("STREAM")
        self._cam.initialize(camurl)
        self._calibrateState = CamCalibrateLoop.CamCalibrateLoop()
        self._mountingState = CamMoutningLoop.CamMountingLoop()
        self._playState = PlayStateLoop.PlayStateLoop()
        self._state = {"PlayState": self._playState, "CalState": self._calibrateState,
                       "MountingState": self._mountingState}

        GPIO.setmode(GPIO.BCM)
        self._buttons = {"GREEN": ArcadeButton.ArchadeButton(GPIO, 8, 7, 0.5, 2),
                         "YELLOW": ArcadeButton.ArchadeButton(GPIO, 14, 15, 0.5, 2),
                         "RED": ArcadeButton.ArchadeButton(GPIO, 23, 24, 0.5, 2),
                         "BLUE": ArcadeButton.ArchadeButton(GPIO, 20, 21, 0.5, 2)}

        # Calfile exists, presuming board and cam already in place
        if os.path.isfile(dartconfig["calibration"]["savepath"]):
            self._currentStateLoop = self._state["CalState"]
        else:
            self._currentStateLoop = self._state["MountingState"]

        self._tmatrix = None
        # TODO: add an IO for red and green button...

    def initialize(self):
        print("Main init...")
        print(r"DartScore:  Copyright (C) 2019 - 2020  Pär Sundbäck, "
              r"mailto:par@sundback.com http://www.github.com/teddycool")
        print("This program comes with ABSOLUTELY NO WARRANTY")
        print("This is free software, and you are welcome to redistribute it under certain conditions")
        print("DartScore is licensed under GPL3. A full description is available in license.md in the root directory")

        for button in self._buttons:
            self._buttons[button].initialize()
            self._buttons[button].activate(True)
            time.sleep(1)

        self.time = time.time()
        self._lastframetime = time.time()
        # Init all states
        for key in self._state.keys():
            self._state[key].initialize()
        # print ("Game started at ", self.time)

    def update(self):
        start = time.time()
        frame = self._cam.update()
        self._currentStateLoop.update(frame, self)
        # print ("Main update time: " + str(time.time()-start))
        # TODO: implement threading!
        # TODO: if green button pressed -> next state
        # TODO: if red button longpressed -> shut down...
        # TODO: Break out gui handling from state-loops to be able to parallize

        return frame

    def draw(self, frame):
        start = time.time()
        frame = self._currentStateLoop.draw(frame)

    # framerate = round(1/(time.time()-self._lastframetime),2)
    # self._lastframetime= time.time()
    # self._vision.draw(frame, framerate) #Actually draw frame to mjpeg streamer...
    # self._gui.draw(frame)
    # print ("Main draw time: " + str(time.time()-start))

    def change_state(self, newstate):
        self._currentStateLoop = self._state[newstate]
        self._currentStateLoop.initialize()
