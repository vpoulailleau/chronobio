import logging
from queue import Queue

import arcade

from chronobio.game.constants import MAX_NB_PLAYERS
from chronobio.viewer.constants import SCREEN_HEIGHT, SCREEN_TITLE, SCREEN_WIDTH
from chronobio.viewer.farm import Farm
from chronobio.viewer.farm_background import FarmBackround
from chronobio.viewer.score import Score

FARM_HEIGHT = SCREEN_HEIGHT * 2 / MAX_NB_PLAYERS

input_queue: Queue = Queue()


class Window(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.csscolor.DARK_OLIVE_GREEN)
        self.background_list: arcade.SpriteList = None
        self.farm_backgrounds: list[FarmBackround] = []
        self.farms: list[Farm] = []
        self.score = Score()

    def setup(self):
        self.background_list = arcade.SpriteList()
        grass = arcade.Sprite("chronobio/viewer/images/grass.jpeg")
        grass_width = grass.width
        grass_height = grass.height
        for x in range(0, SCREEN_WIDTH, grass_width):
            for y in range(0, SCREEN_HEIGHT, grass_height):
                grass = arcade.Sprite("chronobio/viewer/images/grass.jpeg")
                grass.position = x + grass_width // 2, y + grass_height // 2
                self.background_list.append(grass)

        self.farm_backgrounds.clear()
        self.farms.clear()
        for n in range(MAX_NB_PLAYERS):
            self.farm_backgrounds.append(
                FarmBackround(
                    x=(1 + n % 2) * SCREEN_WIDTH / 3 - 40,
                    y=(n // 2 + 0.5) * FARM_HEIGHT,
                    player=n,
                    angle=0,
                )
            )
            self.farms.append(
                Farm(
                    x=(1 + n % 2) * SCREEN_WIDTH / 3 - 40,
                    y=(n // 2 + 0.5) * FARM_HEIGHT,
                    angle=0,
                )
            )

    def on_draw(self):
        if not input_queue.empty():
            data = input_queue.get()
            for index, farm in enumerate(self.farms):
                farm.update(data["farms"][index])
                farm.update_climate(data["events"])
            self.score.update(data)

        self.clear()
        self.background_list.draw()
        for farm_background in self.farm_backgrounds:
            farm_background.draw()
        for farm in self.farms:
            farm.draw()
        self.score.draw()


def gui_thread():
    window = Window()
    try:
        window.setup()
        arcade.run()
    except Exception:  # noqa: PIE786
        logging.exception("uncaught exception")
