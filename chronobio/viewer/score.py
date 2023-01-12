from dataclasses import dataclass
from typing import Optional

import arcade

from chronobio.game.constants import MAX_NB_PLAYERS
from chronobio.viewer.constants import SCREEN_HEIGHT, SCREEN_WIDTH, EVENT_VISIBILITY_NB_DAYS, COLORS

MARGIN = 20
WIDTH = SCREEN_WIDTH / 3 - 2 * MARGIN
HEIGHT = SCREEN_HEIGHT - 2 * MARGIN
CENTER_X = SCREEN_WIDTH / 6
CENTER_Y = SCREEN_HEIGHT / 2
NAME_OFFSET = 30
SCORE_OFFSET = NAME_OFFSET - 20
DATE_OFFSET = SCREEN_HEIGHT - 2 * MARGIN - 20
DATE_HEIGHT = 40
MESSAGES_HEIGHT = 300
MESSAGES_OFFSET = DATE_OFFSET - 40
SCORES_HEIGHT = (HEIGHT - DATE_HEIGHT - 2 * MARGIN - MESSAGES_HEIGHT)
SCORES_OFFSET = 2 * MARGIN


def day2date(day_number: int) -> tuple[int, int, int]:
    """Generate date (y, m, d)"""
    day = day_number % 30 + 1
    month = day_number // 30
    year = month // 12 + 1
    month = month % 12 + 1
    return year, month, day


@dataclass
class Message:
    message: str
    day: int
    player: int
    arcade_text: Optional[arcade.Text] = None


class Score:
    def __init__(self):
        self.state: dict = {}
        self.messages: list[Message] = [Message("let the best team win!", 0, -1)]

    def update(self, game_state: dict) -> None:
        self.state = game_state

        day = self.state["day"]
        for message in self.state["events"]:
            self.messages.append(Message(message, day, player=-1))
        for index, farm in enumerate(self.state["farms"]):
            name = farm["name"]
            for message in farm["events"]:
                self.messages.append(Message(f"{name}: {message}", day, player=index))

        removed = False
        for message in self.messages[:]:
            if day > message.day + EVENT_VISIBILITY_NB_DAYS:
                self.messages.remove(message)
                removed = True
        if removed:
            for message in self.messages:
                message.arcade_text = None

    def draw(self) -> None:
        arcade.draw_rectangle_filled(
            center_x=CENTER_X,
            center_y=CENTER_Y,
            width=WIDTH,
            height=HEIGHT,
            color=(255, 255, 255, 130),
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
                + SCORES_OFFSET
                + SCORES_HEIGHT / (MAX_NB_PLAYERS) * n,
                color=COLORS[n],
                font_size=20,
                font_name="Kenney Blocks",
            )
            score = self.state["farms"][n]["score"]
            arcade.draw_text(
                f"Score: {score:,d}".replace(",", " "),
                start_x=MARGIN * 2,
                start_y=SCORE_OFFSET
                + SCORES_OFFSET
                + SCORES_HEIGHT / (MAX_NB_PLAYERS) * n,
                color=COLORS[n],
                font_size=14,
                font_name="Kenney Future",
            )

        arcade.draw_text(
            "Events",
            start_x=MARGIN * 2,
            start_y=MESSAGES_OFFSET,
            color=arcade.color.BROWN_NOSE,
            font_size=20,
            font_name="Kenney Blocks",
        )
        for index, message in enumerate(self.messages[:5]):
            if message.arcade_text is None:
                message.arcade_text = arcade.Text(
                    f"- {message.message:.130}",
                    start_x=MARGIN * 2,
                    start_y=MESSAGES_OFFSET - 30 - index * 60,
                    color=COLORS[message.player],
                    font_size=12,
                    font_name="Kenney Future",
                    multiline=True,
                    width=int(WIDTH - 2 * MARGIN)
                )
            message.arcade_text.draw()
