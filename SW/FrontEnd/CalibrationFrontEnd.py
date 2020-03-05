__author__ = 'teddycool'
# This file is part of the DartScore project created by Pär Sundbäck
# More at https://github.com/teddycool/DartScore
#
# Purpose of this file:
# GUI for the calibration state

import sys
import pygame
import numpy as np
import Cam
from cv2 import cv2
from DartScoreEngine.DartScoreEngineConfig import dartconfig
from FrontEnd import FrontEndBase
sys.path.append("/home/pi/DartScore/SW")


class CalibrationFrontEnd(FrontEndBase.FrontEndBase):

    def __init__(self):
        super(CalibrationFrontEnd, self).__init__()
        self._myreallybigfont = pygame.font.SysFont("Comic", 150)
        self._mybigfont = pygame.font.SysFont("Comic", 100)
        self._dslabel = self._myreallybigfont.render("* DartScore *", 3, (0, 255, 0))
        self._cam1label = self._myreallybigfont.render("Camera 1 stream", 3, (0, 255, 0))
        self._cam2label = self._myreallybigfont.render("Camera 2 stream", 3, (0, 255, 0))

    def update(self, stateinfostruct):
        pass

    def draw(self, frame1, frame2=None):
        black = 0, 0, 0
        frame1 = np.rot90(frame1)
        frame1 = np.flipud(frame1)
        frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
        frame1 = pygame.surfarray.make_surface(frame1)
        self.screen.fill(black)
        self.screen.blit(frame1, (300, 200))
        self.screen.blit(self._dslabel, (500, 20))
        self.screen.blit(self._cam1label, (300, 900))
        if frame2 is not None:
            frame2 = np.rot90(frame2)
            frame2 = np.flipud(frame2)
            frame2 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
            frame2 = pygame.surfarray.make_surface(frame2)
            self.screen.fill(black)
            self.screen.blit(frame2, (300, 800))
            self.screen.blit(self._dslabel, (500, 20))
            # self.screen.blit(self._cam1label, (300, 900))

        pygame.display.flip()


# Testcode to run module. Standard Python way of testing modules.
# 1680x1050 (16:10)
if __name__ == "__main__":

    cap = Cam.create_cam("STREAM")
    cap.initialize(dartconfig["cam"]["camurl"])

    gl = CalibrationFrontEnd()
    stopped = False
    while not stopped:    # Capture frame-by-frame
        frame = cap.update()
        gl.update(None)
        gl.draw(frame)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                stopped = True

    pygame.quit()
