from chronobio.game.vegetable import Vegetable


class Field:
    def __init__(self):
        self.content = Vegetable.NONE
        self.needed_water = 0