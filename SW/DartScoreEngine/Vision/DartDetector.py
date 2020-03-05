__author__ = 'teddycool'
# This file is part of the DartScore project created by Pär Sundbäck
# More at https://github.com/teddycool/DartScore
#
# Purpose of this file:
# Detect when a dart hits the board and when the board is empty. Wait until dart has stopped (2 similar frames)
# The bounding rect for the new dart is used by DartHit to figure out the coordinates for the hit and calsulate scores

import sys
import time
import pygame
import numpy as np
import Cam
from cv2 import cv2
from DartScoreEngine.DartScoreEngineConfig import dartconfig
from DartScoreEngine.Vision.DartHit import DartHit
from FrontEnd import GameFrontEnd
sys.path.append("/home/pi/DartScore/SW")


class DartDetector(object):

    def __init__(self, boardemptyframe):
        self._boundingRects = []
        self._rawCnts = []
        self._boardEmptyFrame = boardemptyframe.copy()
        self._seqno = 0
        self._lastscore = None
        self._lasthitcoords = None
        self._darthit = DartHit()

    def board_empty(self, frame):
        # print ("Board empty?")
        cnts = self._frameDeltaBoundingBoxes(self._boardEmptyFrame, frame)
        return len(cnts) == 0

    def board_changed(self, frame1, frame2):
        # print ("Board changed?")
        cnts = self._frameDeltaBoundingBoxes(frame1, frame2)
        return len(cnts) > 0

    def detect_dart(self, currentframe, previousframe):
        # print ("Dart detected?")
        self._boundingRects, thresh, cnts = self._dartDelta(currentframe, previousframe)
        if len(self._boundingRects) > 0:
            self._lasthitcoords, self._lastscore = self._darthit.update(thresh, cnts)
            rectno = 0
            # # TODO: refactor this...
            # for rect in self._boundingRects:
            #     # TODO: Check for the dart template in the frame...
            #     x,y,w,h = rect
            #     x1 = x+w
            #     y1 = y+h
            #     cropped = currentframe[y:y1, x:x1]
            #     self._lasthitcoords, self._lastscore = self._darthit.update(thresh, cnts)
            #     print ("Hitrect: " + str(rect))
            #     if dartconfig["DartHit"]["WriteFramesToSeparateFiles"]:
            #         cv2.imwrite("dhframe"+str(self._seqno)+ "_" +str(rectno) +".jpg",cropped)
            #         rectno = rectno +1
            # self._seqno=self._seqno+1
        return len(self._boundingRects)> 0

    def draw(self, frame):
        # print ("Draw dart")
        # for (x, y, w, h) in self._boundingRects:
        #    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        frame = self._darthit.draw(frame)
        return frame

    def _prepareFrame(self,frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), cv2.BORDER_DEFAULT)
        return gray

    def _dartDelta(self, frame1, frame2):
        boundingRects = []
        rawCnts = []
        gray1 = self._prepareFrame(frame1)
        gray2 = self._prepareFrame(frame2)
        # compute the absolute difference between the frames
        frameDelta = cv2.absdiff(gray1, gray2)

        ret, thresh = cv2.threshold(frameDelta, 30, 200, cv2.THRESH_BINARY)
        thresh = cv2.dilate(thresh, None, iterations=2)
        cv2.imwrite("ddframe" + str(self._seqno) + ".jpg", thresh)
        self._seqno = self._seqno+1
        img, cnts, hierarch = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) > dartconfig["DartHit"]["DartHitMinArea"]:
                if cv2.contourArea(c) < dartconfig["DartHit"]["DartHitMaxArea"]:
                    rect = cv2.boundingRect(c)
                    boundingRects.append(rect)
                    rawCnts.append(c)
        return boundingRects, thresh,  rawCnts


    def _frameDeltaBoundingBoxes(self, frame1, frame2):
        bounding_rects = []
        gray1 = self._prepareFrame(frame1)
        gray2 = self._prepareFrame(frame2)
        raw_cnts = []

        # compute the absolute difference between the frames
        frame_delta = cv2.absdiff(gray1, gray2)
        ret, thresh = cv2.threshold(frame_delta, 30, 200, cv2.THRESH_BINARY)
        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        img, cnts, hierarch = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # loop over the contours
        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) > dartconfig["DartHit"]["DartHitMinArea"]:
                rect = cv2.boundingRect(c)
                bounding_rects.append(rect)
                raw_cnts = cnts
        return bounding_rects


if __name__ == '__main__':
    print("Testcode for DartFinder")

    gl = GameFrontEnd.GameFrontEnd()

    cam = Cam.create_cam("STREAM")
    cam.initialize(dartconfig["cam"]["camurl"])

    transform = np.float32([[1.78852294e+00, -1.10143263e-01, -4.85063747e+02],
                            [2.17855239e-01,  1.03682933e+00, -3.82665632e+01],
                            [1.28478485e-03, -1.58506840e-04,  1.00000000e+00]])
    cam.set_transform_matrix(transform)

    frame1 = cam.update()
    time.sleep(0.1)
    dd = DartDetector(frame1)  # Empty board expected!
    previousframe = cam.update()
    currentframe = cam.update()

    while True:
        frame = cam.update()
        currentframe = frame.copy()

        if not dd.board_empty(currentframe):
            if dd.board_changed(currentframe, previousframe):
                if dd.detect_dart(currentframe, previousframe):
                    currentframe = dd.draw(currentframe)

        gl.draw(currentframe)
        previousframe = frame.copy()

        for event in pygame.event.get():
            # print(pygame.event.event_name(event.type))
            if pygame.event.event_name(event.type).count('Quit') > 0:
                pygame.quit()
                break
