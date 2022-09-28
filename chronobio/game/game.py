import random

from chronobio.game.constants import CLIMATE_DISASTER_THRESHOLD, MAX_NB_PLAYERS
from chronobio.game.farm import Farm
from chronobio.game.location import Location


class Game:
    def __init__(self: "Game") -> None:
        self.farms = [Farm() for _ in range(MAX_NB_PLAYERS)]
        self.greenhouse_gas = 0

    def add_player(self, name: str) -> None:
        for farm in self.farms:
            if not farm.name:
                farm.name = name
                farm.blocked = False
                break

    def new_day(self: "Game") -> None:
        self.climate_change()
        for farm in self.farms:
            if farm.blocked:
                continue
            farm.income()
            farm.pollute(self)

    def climate_change(self: "Game") -> None:
        disaster = (
            random.randint(0, self.greenhouse_gas**2) > CLIMATE_DISASTER_THRESHOLD
        )
        if disaster:
            kind = random.choice(["flood", "frost", "heat wave", "fire"])
            impacted_locations = [random.randint(0, 1) for _ in range(len(Location))]
            fields = (
                Location.FIELD1,
                Location.FIELD2,
                Location.FIELD3,
                Location.FIELD4,
                Location.FIELD5,
            )

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
