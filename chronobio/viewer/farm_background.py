import math

import arcade

from chronobio.viewer.constants import SCREEN_HEIGHT, SCREEN_WIDTH

CENTER_X = SCREEN_WIDTH // 2
CENTER_Y = SCREEN_HEIGHT // 2
FARM_LENGTH = min(CENTER_X, CENTER_Y)

SOUP_FACTORY_DISTANCE_FROM_CENTER = FARM_LENGTH / 7
SOUP_FACTORY_WIDTH = FARM_LENGTH / 6

FIELD_OFFSET = FARM_LENGTH / 7 * 2
FIELD_WIDTH = FARM_LENGTH / 8
FIELD_DISTANCE = FARM_LENGTH / 7

FARM_BUILDING_DISTANCE_FROM_CENTER = FARM_LENGTH
FARM_BUILDING_WIDTH = FARM_LENGTH / 7


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

        for field_index in range(5):
            field = arcade.Sprite("chronobio/viewer/images/field.jpg")
            field.position = self.rotate(FIELD_OFFSET + field_index * FIELD_DISTANCE, 0)
            field.width = FIELD_WIDTH
            field.height = 2 * FIELD_WIDTH
            field.angle = angle
            self.sprite_list.append(field)

        farm = arcade.Sprite("chronobio/viewer/images/farm.png")
        farm.position = self.rotate(FARM_BUILDING_DISTANCE_FROM_CENTER, 0)
        farm.width = FARM_BUILDING_WIDTH
        farm.height = FARM_BUILDING_WIDTH
        farm.angle = angle
        self.sprite_list.append(farm)

    def rotate(self, x, y):
        cos = math.cos(math.radians(self.angle))
        sin = math.sin(math.radians(self.angle))
        return cos * x - sin * y + CENTER_X, sin * x + cos * y + CENTER_Y
