from chronobio.game.constants import (
    DAYS_OFF_PER_FIRE,
    DAYS_OFF_PER_FLOOD,
    VEGETABLE_PER_STOCK_DELIVERY,
)
from chronobio.game.vegetable import Vegetable


class SoupFactory:
    def __init__(self: "SoupFactory") -> None:
        self.days_off = 0
        self.stock: dict[Vegetable, int] = {
            vegetable: 0 for vegetable in Vegetable if vegetable != Vegetable.NONE
        }

    def state(self: "SoupFactory") -> dict:
        return {
            "days_off": self.days_off,
            "stock": {vegetable.name: stock for vegetable, stock in self.stock.items()},
        }

    def flood(self: "SoupFactory") -> None:
        self.days_off += DAYS_OFF_PER_FLOOD

    def fire(self: "SoupFactory") -> None:
        self.days_off += DAYS_OFF_PER_FIRE

    def deliver(self: "SoupFactory", vegetable: Vegetable) -> None:
        if vegetable == Vegetable.NONE:
            return
        self.stock[vegetable] += VEGETABLE_PER_STOCK_DELIVERY
