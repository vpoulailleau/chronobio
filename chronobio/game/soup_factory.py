from chronobio.game.constants import (
    DAYS_OFF_PER_FIRE,
    DAYS_OFF_PER_FLOOD,
    VEGETABLE_PER_STOCK_DELIVERY,
)
from chronobio.game.vegetable import Vegetable

# TODO manage day off


class SoupFactory:
    def __init__(self):
        self.days_off = 0
        self.stock: dict[Vegetable, int] = {
            vegetable: 0 for vegetable in Vegetable if vegetable != Vegetable.NONE
        }

    def state(self: "SoupFactory") -> dict:
        return {
            "days_off": self.days_off,
            "stock": self.stock,
        }

    def flood(self: "SoupFactory") -> None:
        self.days_off += DAYS_OFF_PER_FLOOD

    def fire(self: "SoupFactory") -> None:
        self.days_off += DAYS_OFF_PER_FIRE

    def deliver(self: "SoupFactory", vegetable: Vegetable) -> None:
        self.stock[vegetable] += VEGETABLE_PER_STOCK_DELIVERY
