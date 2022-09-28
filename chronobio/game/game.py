from chronobio.game.constants import MAX_NB_PLAYERS
from chronobio.game.farm import Farm


class Game:
    def __init__(self: "Game") -> None:
        self.farms = [Farm() for _ in range(MAX_NB_PLAYERS)]
        self.greenhouse_gas = 0

    def add_player(self, name: str) -> None:
        for farm in self.farms:
            if not farm.name:
                farm.name = name
                farm.blocked = False

    def new_day(self: "Game") -> None:
        for farm in self.farms:
            if farm.blocked:
                continue
            farm.income()
            farm.pollute(self)
