import arcade

from chronobio.game.constants import MAX_NB_PLAYERS
from chronobio.viewer.constants import SCREEN_HEIGHT, SCREEN_WIDTH

MARGIN = 20
WIDTH = SCREEN_WIDTH / 3 - 2 * MARGIN
HEIGHT = SCREEN_HEIGHT - 2 * MARGIN
CENTER_X = SCREEN_WIDTH / 6
CENTER_Y = SCREEN_HEIGHT / 2
NAME_OFFSET = 50
SCORE_OFFSET = NAME_OFFSET - 30
DATE_OFFSET = SCREEN_HEIGHT - 2 * MARGIN - 20
DATE_HEIGHT = 40


def day2date(day_number: int) -> tuple[int, int, int]:
    """Generate date (y, m, d)"""
    day = day_number % 30 + 1
    month = day_number // 30
    year = month // 12 + 1
    month = month % 12 + 1
    return year, month, day


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
            return  # game not started

        year, month, day = day2date(self.state["day"])
        date = f"{day}/{month}/{year:04d}"
        arcade.draw_text(
            date,
            start_x=MARGIN * 2,
            start_y=DATE_OFFSET,
            color=arcade.color.BROWN_NOSE,
            font_size=20,
            font_name="Kenney Blocks",
        )

        for n in range(MAX_NB_PLAYERS):
            arcade.draw_text(
                self.state["farms"][n]["name"][:22],
                start_x=MARGIN * 2,
                start_y=NAME_OFFSET
                + MARGIN * 2
                + (HEIGHT - DATE_HEIGHT - 2 * MARGIN) / (MAX_NB_PLAYERS) * n,
                color=arcade.color.BROWN_NOSE,
                font_size=20,
                font_name="Kenney Blocks",
            )
            score = self.state["farms"][n]["score"]
            arcade.draw_text(
                f"Score: {score:,d}".replace(",", " "),
                start_x=MARGIN * 2,
                start_y=SCORE_OFFSET
                + MARGIN * 2
                + (HEIGHT - DATE_HEIGHT - 2 * MARGIN) / (MAX_NB_PLAYERS) * n,
                color=arcade.color.BROWN_NOSE,
                font_size=14,
                font_name="Kenney Future",
            )