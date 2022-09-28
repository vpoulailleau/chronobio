from chronobio.game.farm import Farm

MAX_NB_PLAYERS = 6
FARM_MONEY_PER_DAY = 30


class Game:
    def __init__(self: "Game"):
        self.farms = [Farm() for i in range(MAX_NB_PLAYERS)]

    def new_day(self: "Game"):
        for farm in self.farms:
            if not farm.blocked:
                farm.money += FARM_MONEY_PER_DAY