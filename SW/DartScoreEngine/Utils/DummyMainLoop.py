__author__ = 'teddycool'
# This file is part of the DartScore project created by Pär Sundbäck
# More at https://github.com/teddycool/DartScore
#
# Purpose of this file:
# Mock needed features in the mainloop for testing purposes. Features are added when needed

import Cam
from DartScoreEngine.DartScoreEngineConfig import dartconfig


class DummyMainLoop(object):
    def __init__(self, camurl=dartconfig["cam"]["camurl"]):
        self._cam = Cam.create_cam("STREAM")
        self._cam.initialize(camurl)
        self._tmatrix = None

    def change_state(self, newstate):
        pass
