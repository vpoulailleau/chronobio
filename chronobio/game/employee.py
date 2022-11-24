import math
from typing import Optional

from chronobio.game.constants import (
    NB_SOUPS_PER_DAY,
    NEEDED_WATER_BEFORE_HARVEST,
    SALARY_RAISE_FACTOR,
    SOUP_PRICES_PER_VETEGABLE,
)
from chronobio.game.location import Location
from chronobio.game.tractor import Tractor
from chronobio.game.vegetable import Vegetable


class Employee:
    def __init__(self: "Employee", farm: "Farm", id: int) -> None:
        self.farm = farm
        self.id: int = id
        self.location: Location = Location.FARM
        self.tractor: Optional[Tractor] = None
        self.salary: int = 1_000
        self.action_to_do: tuple = tuple()
        self._stock_vegetable: Vegetable = Vegetable.NONE

    def _move(self: "Employee", target: Location) -> None:
        distance = abs(target - self.location)
        sign = 1 if target > self.location else -1
        if not distance:
            return
        if self.tractor is None:
            self.location += sign
        else:
            if distance > 3:
                self.location += sign * 3
            else:
                self.location = target
            self.tractor.location = self.location

        # clamp location to valid location
        if self.location < Location.FARM:
            self.location = Location.FARM
        if self.location > Location.SOUP_FACTORY:
            self.location = Location.SOUP_FACTORY
        self.location = Location(self.location)
        if self.tractor is not None:
            self.tractor.location = self.location

    def raise_salary(self: "Employee") -> None:
        self.salary *= SALARY_RAISE_FACTOR
        self.salary = math.ceil(self.salary)

    def do_action(self: "Employee") -> None:
        if not self.action_to_do:
            return

        if self.action_to_do[0] == "SOW":
            vegetable, field = self.action_to_do[1:]
            self._move(field.location)
            if self.location != field.location:
                return  # no yet in the field
            field.needed_water = NEEDED_WATER_BEFORE_HARVEST
            field.content = vegetable
            self.action_to_do = tuple()

        elif self.action_to_do[0] == "WATER":
            field = self.action_to_do[1]
            self._move(field.location)
            if self.location != field.location:
                return  # not yet in the field
            if field.content:
                field.needed_water = max(0, field.needed_water - 1)
            self.action_to_do = tuple()

        elif self.action_to_do[0] == "STOCK":
            field, tractor, step = self.action_to_do[1:]
            if step == 0:
                if self.location != tractor.location:
                    self._move(tractor.location)
                else:
                    step = 1

            if step == 1:
                if any(
                    empl.tractor == tractor and empl != self
                    for empl in self.farm.employees
                ):
                    self.farm.invalid_action(f"Tractor {tractor.id} is already used.")
                self.tractor = tractor
                print(field)
                if self.location != field.location:
                    self._move(field.location)
                else:
                    step = 2

            if step == 2:
                if not field.content or field.needed_water:
                    self.action_to_do = tuple()  # cancel action
                    return
                else:
                    step = 3

            if step == 3:
                if self.location != Location.SOUP_FACTORY:
                    self._move(Location.SOUP_FACTORY)
                else:
                    step = 4

            if step == 4:
                self._stock_vegetable = field.content  # TODO lock field during delivery
                field.content = Vegetable.NONE
                field.needed_water = 0
                self.farm.soup_factory.deliver(self._stock_vegetable)
                self._stock_vegetable = Vegetable.NONE
                self.action_to_do = tuple()
                return

            self.action_to_do = ("STOCK", field, tractor, step)

        elif self.action_to_do[0] == "COOK":
            self._move(Location.SOUP_FACTORY)
            if self.location != Location.SOUP_FACTORY:
                return  # not yet in the factory
            if self.tractor is not None:
                self.tractor = None  # no tractor in soup factory!
            if sum(self.farm.soup_factory.stock.values()):
                nb_vegetables = 0
                for vegetable in Vegetable:
                    if vegetable == Vegetable.NONE:
                        continue
                    if self.farm.soup_factory.stock[vegetable]:
                        self.farm.soup_factory.stock[vegetable] -= NB_SOUPS_PER_DAY
                        nb_vegetables += 1
                self.farm.money += (
                    SOUP_PRICES_PER_VETEGABLE[nb_vegetables] * NB_SOUPS_PER_DAY
                )
                plural = "s" if nb_vegetables > 1 else ""
                self.farm.event_messages.append(
                    f"[SOUP] {nb_vegetables} vegetable{plural}"
                )
            self.action_to_do = tuple()

    def state(self: "Employee") -> dict:
        tractor_state = None if self.tractor is None else self.tractor.state()
        return {
            "id": self.id,
            "location": self.location.name,
            "tractor": tractor_state,
            "salary": self.salary,
        }

    def __repr__(self: "Employee") -> str:
        return f"Employee(id={self.id}, salary={self.salary}, location={self.location.name}, tractor={self.tractor})"
