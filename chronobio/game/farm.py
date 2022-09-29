from chronobio.game.constants import (
    FARM_MONEY_PER_DAY,
    FIELD_MONEY_PER_DAY,
    FIELD_PRICE,
    GREENHOUSE_GAS_PER_TRACTOR,
    NEEDED_WATER_BEFORE_HARVEST,
)
from chronobio.game.employee import Employee
from chronobio.game.field import Field
from chronobio.game.location import fields
from chronobio.game.soup_factory import SoupFactory
from chronobio.game.tractor import Tractor
from chronobio.game.vegetable import Vegetable


class Farm:
    def __init__(self: "Farm") -> None:
        self.blocked: bool = True
        self.name: str = ""
        self.money: int = 100_000
        self.fields: list[Field] = [Field(location) for location in fields]
        self.tractors: list[Tractor] = []
        self.soup_factory: SoupFactory = SoupFactory()
        self.employees: list[Employee] = []
        self.next_employee_id = 1

    def income(self: "Farm") -> None:
        self.money += FARM_MONEY_PER_DAY
        for field in self.fields:
            if field.content != Vegetable.NONE:
                self.money += FIELD_MONEY_PER_DAY

    def expend(self: "Farm", day: int) -> None:
        if day % 30 == 0:
            for employee in self.employees:
                if self.money < employee.salary:
                    raise ValueError(f"Not enough money to pay employee {employee.id}.")
                else:
                    self.money -= employee.salary
                employee.raise_salary()

    def pollute(self: "Farm", game: "chronobio.game.game.Game") -> None:
        game.greenhouse_gas += len(self.tractors) * GREENHOUSE_GAS_PER_TRACTOR

    @property
    def score(self: "Farm") -> int:
        return self.money

    def get_employee(self: "Farm", employee_id: int) -> Employee:
        for em in self.employees:
            if employee_id == em.id:
                employee = em
                break
        else:
            employee = None
        if employee is None:
            raise ValueError(f"No employee with ID: {employee_id}.")
        return employee

    def get_field(self: "Farm", location_id: int) -> Field:
        if not (1 <= location_id <= 5):
            raise ValueError(f"Invalid field ID: {location_id}.")
        return self.fields[location_id - 1]

    @staticmethod
    def get_vegetable(vegetable_name: str) -> Vegetable:
        translations = {
            "PATATE": "POTATO",
            "POIREAU": "LEEK",
            "TOMATE": "TOMATO",
            "OIGNON": "ONION",
            "COURGETTE": "ZUCCHINI",
        }
        vegetable_enum = translations.get(vegetable_name)
        if vegetable_enum is None:
            raise ValueError(f"Unknown vegetable: {vegetable_name}.")
        return Vegetable.__members__[vegetable_enum]

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

    def _acheter_champ(self: "Farm", owner: str) -> None:
        for field in self.fields:
            if not field.bought:
                if self.money >= FIELD_PRICE:
                    field.bought = True
                    self.money -= FIELD_PRICE
                    return
                raise ValueError("Not enough money to buy field.")
        raise ValueError("No more field available")

    def _semer(
        self: "Farm", employee_id: str, vegetable_name: str, location_id: str
    ) -> None:
        employee = self.get_employee(int(employee_id))
        field = self.get_field(int(location_id))
        vegetable = self.get_vegetable(vegetable_name)

        if employee.days_off:
            raise ValueError(f"Employee {employee_id} is already busy.")
        # TODO vérifier que le champ est acheté
        print("semer", employee, vegetable, field)
        employee.move(
            field.location
        )  # TODO à revoir, comment stocker la liste d'actions à faire ?
        field.needed_water = NEEDED_WATER_BEFORE_HARVEST
        field.content = vegetable

    def _employer(self: "Farm", owner: int) -> None:
        self.employees.append(Employee(id=self.next_employee_id))
        self.next_employee_id += 1
