__author__ = 'teddycool'
# This file is part of the DartScore project created by Pär Sundbäck
# More at https://github.com/teddycool/DartScore

# Purpose of this file:
# Create a stream of frames from a video feed (networked cam) that can be used by opencv
# REF: https://benhowell.github.io/guide/2015/03/09/opencv-and-web-cam-streaming

import time
import numpy as np
from urllib.request import urlopen
from cv2 import cv2
from DartScoreEngine.DartScoreEngineConfig import dartconfig


class StreamCam(object):

    def __int__(self):
        self._camId = 0

    def initialize(self, camurl):
        print("Stream CAM init...")
        self._actualFrameRate = 0
        self._lastFrameTime = time.time()
        self._stream = urlopen(camurl)
        self._bytes = bytearray()
        self._transform = []

    def update(self):
        while True:
            # TODO: fix configurable cam res
            self._bytes += self._stream.read(1024)
            a = self._bytes.find(b'\xff\xd8')
            b = self._bytes.find(b'\xff\xd9')
            if a != -1 and b != -1:
                jpg = self._bytes[a:b+2]
                self._bytes = self._bytes[b+2:]
                frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                self._actualFrameRate = 1/(time.time()- self._lastFrameTime)
                self._lastFrameTime = time.time()
                if len(self._transform) == 0:
                    return frame
                else:
                    return cv2.warpPerspective(frame, self._transform, (500, 500))

    def set_transform_matrix(self, matrix):
        self._transform = matrix


if __name__ == '__main__':
    print("Testcode for StreamCam")
    cam = StreamCam()
    cam.initialize(dartconfig["cam"]["camurl"])

    while True:
        img = cam.update()
        cv2.imshow('Video', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
