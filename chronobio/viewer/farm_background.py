import math

import arcade

from chronobio.viewer.constants import SCREEN_HEIGHT, SCREEN_WIDTH

CENTER_X = SCREEN_WIDTH // 2
CENTER_Y = SCREEN_HEIGHT // 2
FARM_LENGTH = min(CENTER_X, CENTER_Y)

SOUP_FACTORY_DISTANCE_FROM_CENTER = FARM_LENGTH / 7
SOUP_FACTORY_WIDTH = FARM_LENGTH / 10


class FarmBackround:
    def __init__(self, angle=0):
        self.angle = angle
        self.sprite_list = arcade.SpriteList()

        soup_factory = arcade.Sprite("chronobio/viewer/images/factory_small.png")
        soup_factory.position = self.rotate(SOUP_FACTORY_DISTANCE_FROM_CENTER, 0)
        soup_factory.width = SOUP_FACTORY_WIDTH
        soup_factory.height = SOUP_FACTORY_WIDTH
        soup_factory.angle = angle

        self.sprite_list.append(soup_factory)

    def rotate(self, x, y):
        cos = math.cos(math.radians(self.angle))
        sin = math.sin(math.radians(self.angle))
        return cos * x - sin * y + CENTER_X, sin * x + cos * y + CENTER_Y
