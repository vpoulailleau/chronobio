from chronobio.game.farm import Farm
from chronobio.game.vegetable import Vegetable

MAX_NB_PLAYERS = 6
FARM_MONEY_PER_DAY = 30
FIELD_MONEY_PER_DAY = 50


class Game:
    def __init__(self: "Game"):
        self.farms = [Farm() for _ in range(MAX_NB_PLAYERS)]

    def new_day(self: "Game"):
        for farm in self.farms:
            if not farm.blocked:
                farm.money += FARM_MONEY_PER_DAY
                for field in farm.fields:
                    if field.content != Vegetable.NONE:
                        farm.money += FIELD_MONEY_PER_DAY