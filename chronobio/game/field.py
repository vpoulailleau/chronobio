from chronobio.game.constants import NEEDED_WATER_BEFORE_HARVEST
from chronobio.game.location import Location
from chronobio.game.vegetable import Vegetable


class Field:
    def __init__(self: "Field", location: Location) -> None:
        self.content = Vegetable.NONE
        self.needed_water = 0
        self.bought = False
        self.location = location

    def frost(self: "Field"):
        self.content = Vegetable.NONE
        self.needed_water = 0

    def heat_wave(self: "Field"):
        if self.content:
            self.needed_water += NEEDED_WATER_BEFORE_HARVEST

    def fire(self: "Field"):
        self.content = Vegetable.NONE
        self.needed_water = 0

    def state(self: "Field") -> dict:
        return {
            "content": self.content.name,
            "needed_water": self.needed_water,
            "bought": self.bought,
            "location": self.location.name,
        }

    def __repr__(self: "Field") -> str:
        return (
            f"Field({self.content.name}, needed_water={self.needed_water}, "
            f"bought={self.bought}, location={self.location.name})"
        )
