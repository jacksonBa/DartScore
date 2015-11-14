__author__ = 'teddycool'
#Config vaues for DartScore. This is the only place for these.

dartconfig = {  "cam": {"res":(640, 480), "id":1, "framerate": 20},                                                                 #CAM settings
                "color":{"sector":(0,255,0),"hit": (255,0,0), "aim":  (0,255,0), "calibrate":(0,0,255), "bullseye": (0,0,255)},     #colors of sectors and markers
                "mounting": {"aimrectx": 80,"aimrecty": 40},                                                                        #values for mounting the cam and center bulls-eye
                "Streamer": {"StreamerImage": "/tmp/stream/pic.jpg", "StreamerLib": "/tmp/stream", "VideoFile": "/home/pi/DartScore/video.mpg"},
                "Button": {"Pressed": 0.5, "LongPressed": 2},
                "Log": {"Level": "Verbose", "LogFile": "/tmp/stream/log.log"},
                "Main": {"MaxFrameRate": 10},
                "Vision": {"WriteFramesToSeparateFiles": False, "PrintFrameRate": True},
              }
