import math
from typing import Optional

from chronobio.game.constants import SALARY_RAISE_FACTOR
from chronobio.game.location import Location
from chronobio.game.tractor import Tractor


class Employee:
    def __init__(self: "Employee", id: int) -> None:
        self.id: int = id
        self.location: Location = Location.FARM
        self.days_off: int = 0
        self.tractor: Optional[Tractor] = None
        self.salary: int = 1_000

    def move(self: "Employee", target: Location) -> None:
        distance = abs(target - self.location)
        sign = 1 if target > self.location else -1
        if not distance:
            return
        if self.tractor is None:
            self.days_off = distance - 1
            self.location += sign
        else:
            self.days_off = (distance - 1) // 3
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

    def raise_salary(self: "Employee") -> None:
        self.salary *= SALARY_RAISE_FACTOR
        self.salary = math.ceil(self.salary)

    def __repr__(self: "Employee") -> str:
        return f"Employee(id={self.id}, salary={self.salary}, location={self.location}, tractor={self.tractor})"
