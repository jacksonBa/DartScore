__author__ = 'teddycool'
# This file is part of the DartScore project created by Pär Sundbäck
# More at https://github.com/teddycool/DartScore

# Purpose of this file:
# A set of common used fuctions and variables to use when testing each module/part of the project

import sys
import platform
from cv2 import cv2
from DartScoreEngine.DartScoreEngineConfig import dartconfig

if platform.node() == 'jackson-VirtualBox':
    # The development pc
    # sys.path.append(r'C:\Users\par\OneDrive\Documents\GitHub\DartScore\SW')
    # videofilepath = r'C:\Users\par\OneDrive\Documents\GitHub\DartScore\Testdata\Videos\dartscore_20191120_174641.avi'
    # recorderfilepath = r'C:\Users\par\OneDrive\Documents\GitHub\DartScore\Testdata\Videos'
    sys.path.append(r'~/dev/DartScore/SW')
    videofilepath = r'~/dev/DartScore/Testdata/Videos/dartscore_20191120_174641.avi'
    recorderfilepath = r'~/dev/DartScore/Testdata/Videos'
    camstreamurl = dartconfig["cam"]["camurl"]
else:
    videofilepath = r'/home/pi/DartScore/Testdata/Videos/dartscore_20191107_152701.avi'


# Create a videocapture replacing the cam feed at test,
def get_test_video_capture():
    cap = cv2.VideoCapture(videofilepath)
    if not cap.isOpened():
        print("Error opening video stream or file")
        return None
    else:
        return cap
