__author__ = 'teddycool'

import math
from cv2 import cv2


# Class to create an array defining 'the perfect board' and a 'normalized' board used later on..
# Actual board is 450 mm in diameter,  1 pixel per mm
class BoardArray(object):

    def __init__(self, center=(250, 250), radius=225):
        self._lines = []
        self._circles = []
        self._center = center
        self._radius = radius

        # Size of each scoring sector on the board
        sector = 2*math.pi/20

        self._point_sectors = [[0.5 * sector, 6], [1.5 * sector, 13], [2.5 * sector, 4], [3.5 * sector, 18],
                               [4.5*sector, 1], [5.5*sector, 20], [6.5*sector, 5], [7.5*sector, 12],
                               [8.5*sector, 9], [9.5*sector, 14], [10.5*sector, 11], [11.5*sector, 8],
                               [12.5*sector, 16], [13.5*sector, 7], [14.5*sector, 19], [15.5*sector, 3],
                               [16.5*sector, 17], [17.5*sector, 2], [18.5*sector, 15], [19.5*sector, 10],
                               [20*sector, 6]]

    def draw(self, img):
        sec_color = (0, 0, 255)  # DartScoreEngineConfig.dartconfig['color']['sector']

        cv2.circle(img, self._center, 225, sec_color, 1)    # outer
        cv2.circle(img, self._center, 170, sec_color, 2)    # outside double
        cv2.circle(img, self._center, 162, sec_color, 2)    # inside double
        cv2.circle(img, self._center, 107, sec_color, 2)    # outside treble
        cv2.circle(img, self._center, 99, sec_color, 2)     # inside treble
        cv2.circle(img, self._center, 16, sec_color, 2)     # 25
        cv2.circle(img, self._center, 6, sec_color, 2)      # Bulls-eye

        # 20 sectors
        sector_angle = 2*math.pi/20
        i = 0
        while i < 20:
            cv2.line(img, self._center, (int(self._center[0] + 170 * math.cos((0.5 + i) * sector_angle)),
                                         int(self._center[1] + 170 * math.sin((0.5 + i) * sector_angle))), sec_color, 2)
            i = i+1
        return img

    # Get the scores for the pixel that was hit by the dart after transform...
    # Calculate polar coordinates and then the scores..
    def getscore(self, hit_point):           # hit_point is a tuple (x,y)
        x = hit_point[0] - self._center[0]
        y = hit_point[1] - self._center[1]
        print("--------------")
        print("Values from getscore:")
        print(hit_point, x, y)

        # Calculate length
        r = math.sqrt(x*x + y*y)
        score_base = None

        # Calculate angle
        if x != 0:
            if y < 0:  # Top right quarter or Top left quarter
                a = math.atan(x/y) + 0.5 * math.pi
            elif y == 0:
                a = 0
            else:  # Low right quarter or Low left quarter
                a = math.atan(x/y) + 1.5 * math.pi
        else:
            if y < 0:
                a = math.pi*1.5
            elif y == 0:
                a = None
            else:
                a = math.pi/2

        # Calculate 'score base'
        for sector in self._point_sectors:
            if a < sector[0]:
                score_base = sector[1]
                break

        # Calculate multiple or center hit
        if r < 6:                   # Bulls-eye
            score = 50
        elif r < 16:                # Center ring
            score = 25
        elif r > 99 and r < 107:    # Triple ring
            score = 3* score_base
        elif r > 162 and r < 170:   # Double ring
            score = 2*score_base
        elif r < 170:              # Some where else on score area = 1*
            score = score_base
        else:
            score = 0               # Outside the score area

        print("Score: " + str(score))
        print("--------------")
        return score


if __name__ == "__main__":
    
    img = cv2.imread("boardarraybg.jpg")
    bf = BoardArray()
    print(bf.getscore((250, 250)))
    print(bf.getscore([250, 80]))
    print(bf.getscore([125, 125]))
    print(bf.getscore([250, 410]))
    print(bf.getscore([250, 85]))
    print(bf.getscore((231, 163)))
    img = bf.draw(img)
    cv2.imshow('img', img)
    cv2.imwrite("perfectboard.jpg", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
