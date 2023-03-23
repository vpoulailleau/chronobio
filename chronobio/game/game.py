import logging
import random

from chronobio.game.constants import (
    CLIMATE_DISASTER_THRESHOLD,
    COMMON_VEGETABLE_LOSS,
    MAX_NB_PLAYERS,
    VEGETABLE_PRICE,
)
from chronobio.game.farm import Farm
from chronobio.game.field import Field
from chronobio.game.location import Location, fields


class Game:
    def __init__(self: "Game") -> None:
        self.farms = [Farm(self, index) for index in range(MAX_NB_PLAYERS)]
        self.greenhouse_gas = 0
        self.day = -1
        self.event_messages: list[str] = []

    @property
    def date(self: "Game") -> tuple[int, int, int]:
        """Generate date (y, m, d)"""
        day = self.day % 30 + 1
        month = self.day // 30
        year = month // 12 + 1
        month = month % 12 + 1
        return year, month, day

    def add_player(self, name: str) -> None:
        for farm in self.farms:
            if not farm.name:
                farm.name = name
                farm.blocked = False
                break

    def new_day(self: "Game") -> None:
        self.day += 1
        for farm in self.farms:
            farm.soup_factory.days_off = max(0, farm.soup_factory.days_off - 1)
        for farm in self.farms:
            farm.income()
            farm.expend(self.day)
            farm.pollute()
            farm.do_actions()
        self.climate_change()

    def clear_event_messages(self: "Game"):
        self.event_messages.clear()
        for farm in self.farms:
            farm.event_messages.clear()

    def log_messages(self: "Game") -> None:
        for message in self.event_messages:
            logging.info(message)
        for farm in self.farms:
            for message in farm.event_messages:
                if "INVALID_ACTION" in message:
                    logging.warning("%s : %s", farm.name, message)
                else:
                    logging.info("%s : %s", farm.name, message)

    def field_price(self: "Game", sold_field: Field) -> int:
        price = VEGETABLE_PRICE + COMMON_VEGETABLE_LOSS
        for farm in self.farms:
            for field in farm.fields:
                if field.content == sold_field.content:
                    price -= COMMON_VEGETABLE_LOSS
        return price

    def climate_change(self: "Game") -> None:
        logging.debug(self.greenhouse_gas)
        disaster = (
            random.randint(-40 * CLIMATE_DISASTER_THRESHOLD, self.greenhouse_gas)
            > CLIMATE_DISASTER_THRESHOLD
        )

        if disaster:
            kind = random.choice(["flood", "frost", "heat wave", "fire"])
            impacted_locations = [random.randint(0, 1) for _ in range(len(Location))]

            if kind == "heat wave":
                for location in fields:
                    if impacted_locations[location]:
                        for farm in self.farms:
                            farm.fields[location - Location.FIELD1].heat_wave()
                        self.event_messages.append(
                            f"[CLIMATE] heat wave for {location.name}"
                        )

            elif kind == "frost":
                for location in fields:
                    if impacted_locations[location]:
                        for farm in self.farms:
                            farm.fields[location - Location.FIELD1].frost()
                        self.event_messages.append(
                            f"[CLIMATE] frost for {location.name}"
                        )

            elif kind == "flood":
                if impacted_locations[Location.SOUP_FACTORY]:
                    for farm in self.farms:
                        farm.soup_factory.flood()
                    self.event_messages.append("[CLIMATE] flood for SOUP_FACTORY")

            elif kind == "fire":
                if impacted_locations[Location.SOUP_FACTORY]:
                    for farm in self.farms:
                        farm.soup_factory.fire()
                    self.event_messages.append("[CLIMATE] fire for SOUP_FACTORY")

                for location in fields:
                    if impacted_locations[location]:
                        for farm in self.farms:
                            farm.fields[location - Location.FIELD1].fire()
                        self.event_messages.append(
                            f"[CLIMATE] fire for {location.name}"
                        )

    def state(self) -> dict:
        return {
            "day": self.day,
            "greenhouse_gas": self.greenhouse_gas,
            "events": self.event_messages,
            "farms": [farm.state() for farm in self.farms],
        }
