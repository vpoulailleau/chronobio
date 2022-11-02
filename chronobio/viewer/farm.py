import math

import arcade


class Farm:
    def __init__(self, x, y, angle=0):
        self.angle = angle
        self.x = x
        self.y = y
        self.sprite_list = arcade.SpriteList()

        # self.sprite_list.append(farm)

    def rotate(self, x, y):
        cos = math.cos(math.radians(self.angle))
        sin = math.sin(math.radians(self.angle))
        return cos * x - sin * y + self.x, sin * x + cos * y + self.y
