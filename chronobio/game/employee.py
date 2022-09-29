import math
from typing import Optional

from chronobio.game.constants import NEEDED_WATER_BEFORE_HARVEST, SALARY_RAISE_FACTOR
from chronobio.game.location import Location
from chronobio.game.tractor import Tractor


class Employee:
    def __init__(self: "Employee", id: int) -> None:
        self.id: int = id
        self.location: Location = Location.FARM
        self.tractor: Optional[Tractor] = None
        self.salary: int = 1_000
        self.action_to_do: tuple = tuple()

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
            self.action_to_do = tuple()  # TODO déplacer puis semer

    def __repr__(self: "Employee") -> str:
        return f"Employee(id={self.id}, salary={self.salary}, location={self.location.name}, tractor={self.tractor})"
