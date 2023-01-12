import math

import arcade

from chronobio.viewer.constants import (
    COLORS,
    FARM_BUILDING_DISTANCE_FROM_CENTER,
    FARM_BUILDING_WIDTH,
    FIELD_DISTANCE,
    FIELD_OFFSET,
    FIELD_WIDTH,
    SOUP_FACTORY_DISTANCE_FROM_CENTER,
    SOUP_FACTORY_WIDTH,
)


class FarmBackround:
    def __init__(self, x, y, player: int, angle=0):
        self.angle = angle
        self.x = x
        self.y = y
        self.player = player
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
        return cos * x - sin * y + self.x, sin * x + cos * y + self.y

    def draw(self):
        position = self.rotate(FARM_BUILDING_DISTANCE_FROM_CENTER, 0)
        arcade.draw_lrtb_rectangle_filled(
            left=position[0] - FARM_BUILDING_WIDTH / 2,
            right=position[0] + FARM_BUILDING_WIDTH / 2,
            top=position[1] + FARM_BUILDING_WIDTH / 2,
            bottom=position[1] - FARM_BUILDING_WIDTH / 2,
            color=COLORS[self.player],
        )

        self.sprite_list.draw()
