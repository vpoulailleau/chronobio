from chronobio.game.constants import (
    FARM_MONEY_PER_DAY,
    FIELD_MONEY_PER_DAY,
    FIELD_PRICE,
    GREENHOUSE_GAS_PER_TRACTOR,
)
from chronobio.game.employee import Employee
from chronobio.game.field import Field
from chronobio.game.location import Location
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
        self.employees: list[Employee] = []

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
            raise ValueError("Unknown action.")
        except TypeError:
            raise ValueError("Action with invalid number of arguments.")

    def _acheter_champ(self, owner):
        for field in self.fields:
            if not field.bought:
                if self.money >= FIELD_PRICE:
                    field.bought = True
                    self.money -= FIELD_PRICE
                    return
                raise ValueError("Not enough money to buy field.")
        raise ValueError("No more field available")

    def _semer(self, employee_id: int, vegetable_name: str, location_id: int):
        employee = None
        for em in self.employees:
            if em.id == employee_id:
                employee = em
                break
        if employee is None:
            raise ValueError(f"No employee with ID: {employee_id}.")
        if employee.days_off:
            raise ValueError(f"Employee {employee_id} is already busy.")

        if not (1 <= location_id <= 5):
            raise ValueError(f"Invalid field ID: {location_id}.")
        location = Location(location_id)

        if vegetable_name not in Vegetable.__members__:
            raise ValueError(f"Unknown vegetable: {vegetable_name}.")
        vegetable = Vegetable.__members__[vegetable_name]

        print("semer", employee, vegetable, location)
        employee.move(
            location
        )  # TODO à revoir, comment stocker la liste d'actions à faire ?
