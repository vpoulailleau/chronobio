from chronobio.game.constants import (
    FARM_MONEY_PER_DAY,
    FIELD_MONEY_PER_DAY,
    FIELD_PRICE,
    GREENHOUSE_GAS_PER_TRACTOR,
)
from chronobio.game.field import Field
from chronobio.game.soup_factory import SoupFactory
from chronobio.game.tractor import Tractor
from chronobio.game.vegetable import Vegetable


class Farm:
    def __init__(self: "Farm") -> None:
        self.blocked: bool = True
        self.name: str = ""
        self.money: int = 100_000
        self.fields: list[Field] = [Field() for _ in range(5)]
        self.tractors: list[Tractor] = []
        self.soup_factory: SoupFactory = SoupFactory()

    def income(self: "Farm") -> None:
        self.money += FARM_MONEY_PER_DAY
        for field in self.fields:
            if field.content != Vegetable.NONE:
                self.money += FIELD_MONEY_PER_DAY

    def pollute(self: "Farm", game: "chronobio.game.game.Game") -> None:
        game.greenhouse_gas += len(self.tractors) * GREENHOUSE_GAS_PER_TRACTOR

    @property
    def score(self: "Farm") -> int:
        return self.money

    def action(self: "Farm", action: str) -> None:
        parts = action.split()
        if len(parts) < 2:
            raise ValueError("An action needs at least two parts.")
        verb = parts.pop(1)
        try:
            getattr(self, "_" + verb.lower())(*parts)
        except AttributeError:
            raise ValueError("Unknown action")

    def _acheter_champ(self, owner):
        for field in self.fields:
            if not field.bought:
                if self.money >= FIELD_PRICE:
                    field.bought = True
                    self.money -= FIELD_PRICE
                    return
                raise ValueError("Not enough money to buy field.")
        raise ValueError("No more field available")