import arcade

from chronobio.game.constants import MAX_NB_PLAYERS
from chronobio.viewer.constants import SCREEN_HEIGHT, SCREEN_WIDTH

MARGIN = 20
WIDTH = SCREEN_WIDTH / 3 - 2 * MARGIN
HEIGHT = SCREEN_HEIGHT - 2 * MARGIN
CENTER_X = SCREEN_WIDTH / 6
CENTER_Y = SCREEN_HEIGHT / 2
NAME_OFFSET = 100


class Score:
    def __init__(self):
        self.state: dict = {}

    def update(self, game_state: dict) -> None:
        self.state = game_state

    def draw(self) -> None:
        arcade.draw_rectangle_filled(
            center_x=CENTER_X,
            center_y=CENTER_Y,
            width=WIDTH,
            height=HEIGHT,
            color=(255, 255, 255, 100),
        )
        if "farms" not in self.state:
            return
        for n in range(MAX_NB_PLAYERS):
            arcade.draw_text(
                self.state["farms"][n]["name"],
                start_x=MARGIN * 2,
                start_y=NAME_OFFSET
                + MARGIN * 2
                + (HEIGHT - 2 * MARGIN) / (MAX_NB_PLAYERS) * n,
                color=arcade.color.BROWN_NOSE,
                font_size=20,
                font_name="Kenney Blocks",
            )
