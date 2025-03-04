import math
from importlib.resources import files

import arcade

from chronobio.viewer.constants import constants


class FarmBackround:
    def __init__(self, x, y, player: int, angle: float = 0) -> None:
        self.angle = angle
        self.x = x
        self.y = y
        self.player = player
        self.sprite_list = arcade.SpriteList()
        position = self.rotate(constants.FARM_BUILDING_DISTANCE_FROM_CENTER, 0)
        self.background: arcade.shape_list.Shape = (
            arcade.shape_list.create_rectangle_filled(
                center_x=position[0],
                center_y=position[1],
                width=constants.FARM_BUILDING_WIDTH,
                height=constants.FARM_BUILDING_WIDTH,
                color=constants.COLORS[self.player],
            )
        )

        soup_factory = arcade.Sprite(
            files("chronobio.viewer").joinpath("images/factory_small.png")
        )
        soup_factory.position = self.rotate(
            constants.SOUP_FACTORY_DISTANCE_FROM_CENTER, 0
        )
        soup_factory.width = constants.SOUP_FACTORY_WIDTH
        soup_factory.height = constants.SOUP_FACTORY_WIDTH
        soup_factory.angle = angle
        self.sprite_list.append(soup_factory)

        for field_index in range(5):
            field = arcade.Sprite(
                files("chronobio.viewer").joinpath("images/field.jpg")
            )
            field.position = self.rotate(
                constants.FIELD_OFFSET + field_index * constants.FIELD_DISTANCE, 0
            )
            field.width = constants.FIELD_WIDTH
            field.height = 2 * constants.FIELD_WIDTH
            field.angle = angle
            self.sprite_list.append(field)

        farm = arcade.Sprite(files("chronobio.viewer").joinpath("images/farm.png"))
        farm.position = self.rotate(constants.FARM_BUILDING_DISTANCE_FROM_CENTER, 0)
        farm.width = constants.FARM_BUILDING_WIDTH
        farm.height = constants.FARM_BUILDING_WIDTH
        farm.angle = angle
        self.sprite_list.append(farm)

    def rotate(self, x, y):
        cos = math.cos(math.radians(self.angle))
        sin = math.sin(math.radians(self.angle))
        return cos * x - sin * y + self.x, sin * x + cos * y + self.y

    def draw(self):
        self.background.draw()
        self.sprite_list.draw()
