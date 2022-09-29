import random

from chronobio.game.constants import CLIMATE_DISASTER_THRESHOLD, MAX_NB_PLAYERS
from chronobio.game.farm import Farm
from chronobio.game.location import Location, fields


class Game:
    def __init__(self: "Game") -> None:
        self.farms = [Farm() for _ in range(MAX_NB_PLAYERS)]
        self.greenhouse_gas = 0
        self.day = -1

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
        self.climate_change()
        for farm in self.farms:
            if farm.blocked:
                continue
            farm.income()
            farm.expend(self.day)
            farm.pollute(self)
            farm.do_actions()

    def climate_change(self: "Game") -> None:
        disaster = (
            random.randint(0, self.greenhouse_gas**2) > CLIMATE_DISASTER_THRESHOLD
        )
        if disaster:
            kind = random.choice(["flood", "frost", "heat wave", "fire"])
            impacted_locations = [random.randint(0, 1) for _ in range(len(Location))]

            if kind == "heat wave":
                for location in fields:
                    if impacted_locations[location]:
                        for farm in self.farms:
                            farm.fields[location - Location.FIELD1].heat_wave()

            elif kind == "frost":
                for location in fields:
                    if impacted_locations[location]:
                        for farm in self.farms:
                            farm.fields[location - Location.FIELD1].frost()

            elif kind == "flood":
                if impacted_locations[Location.SOUP_FACTORY]:
                    for farm in self.farms:
                        farm.soup_factory.flood()

            elif kind == "fire":
                if impacted_locations[Location.SOUP_FACTORY]:
                    for farm in self.farms:
                        farm.soup_factory.fire()
