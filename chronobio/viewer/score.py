import arcade

from chronobio.viewer.constants import SCREEN_HEIGHT, SCREEN_WIDTH


class Score:
    def __init__(self):
        self.sprite_list = arcade.SpriteList()

        # soup_factory = arcade.Sprite("chronobio/viewer/images/factory_small.png")
        # soup_factory.position = self.rotate(SOUP_FACTORY_DISTANCE_FROM_CENTER, 0)
        # soup_factory.width = SOUP_FACTORY_WIDTH
        # soup_factory.height = SOUP_FACTORY_WIDTH
        # soup_factory.angle = angle
        # self.sprite_list.append(soup_factory)

    def update(self, game_state: dict) -> None:
        self.sprite_list.clear()

    def draw(self) -> None:
        # arcade.draw_text("draw_filled_rect", 363, 3, arcade.color.BLACK, 10)
        arcade.draw_rectangle_filled(
            center_x=SCREEN_WIDTH / 6,
            center_y=SCREEN_HEIGHT / 2,
            width=SCREEN_WIDTH / 3 - 40,
            height=SCREEN_HEIGHT - 40,
            color=(255, 255, 255, 100),
        )
