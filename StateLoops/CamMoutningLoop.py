_author__ = 'teddycool'
import pygame
from  StateLoop import StateLoop
import DartScoreConfig

class CamMountingLoop(StateLoop):
    def __init__(self):
        super(CamMountingLoop, self).__init__()
        return

    def initialize(self):
        width, height= DartScoreConfig.config['cam']['res']
        aimx = DartScoreConfig.config['mounting']['aimrectx']
        aimy = DartScoreConfig.config['mounting']['aimrecty']
        self._centerRect = pygame.Rect(width/2-aimx/2, height/2-aimy/2, aimx, aimy)
        self._centerBullseye = (width/2,  height/2)
        return

    def update(self, screen):
        return screen

    def draw(self, snapshot):
        #draw rect for center of snapshot
        pygame.draw.rect(snapshot, DartScoreConfig.config['color']['aim'], self._centerRect, 5)
        pygame.draw.circle(snapshot, (255,0,0), self._centerBullseye, 3, 0)
        return snapshot