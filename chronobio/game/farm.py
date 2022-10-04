from chronobio.game.constants import (
    FARM_MONEY_PER_DAY,
    FIELD_MONEY_PER_DAY,
    FIELD_PRICE,
    GREENHOUSE_GAS_PER_TRACTOR,
    NB_DAYS_TO_HARVEST,
    TRACTOR_PRICE,
)
from chronobio.game.employee import Employee
from chronobio.game.field import Field
from chronobio.game.location import fields
from chronobio.game.soup_factory import SoupFactory
from chronobio.game.tractor import Tractor
from chronobio.game.vegetable import Vegetable


class Farm:
    def __init__(self: "Farm", game: "Game") -> None:
        self.game = game
        self.blocked: bool = True
        self.name: str = ""
        self.money: int = 100_000
        self.fields: list[Field] = [Field(location) for location in fields]
        self.tractors: list[Tractor] = []
        self.soup_factory: SoupFactory = SoupFactory()
        self.employees: list[Employee] = []
        self.next_employee_id: int = 1
        self.next_tractor_id: int = 1
        self.action_to_do: tuple = tuple()

    def income(self: "Farm") -> None:
        self.money += FARM_MONEY_PER_DAY
        for field in self.fields:
            if field.content != Vegetable.NONE:
                self.money += FIELD_MONEY_PER_DAY

    def expend(self: "Farm", day: int) -> None:
        if day % 30 == 0 and day != 0:
            for employee in self.employees:
                if self.money < employee.salary:
                    raise ValueError(f"Not enough money to pay employee {employee.id}.")
                else:
                    self.money -= employee.salary
                employee.raise_salary()

    def pollute(self: "Farm") -> None:
        self.game.greenhouse_gas += len(self.tractors) * GREENHOUSE_GAS_PER_TRACTOR

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

    def get_tractor(self: "Farm", tractor_id: int) -> Tractor:
        for tr in self.tractors:
            if tractor_id == tr.id:
                tractor = tr
                break
        else:
            tractor = None
        if tractor is None:
            raise ValueError(f"No tractor with ID: {tractor_id}.")
        return tractor

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

    def do_actions(self: "Farm") -> None:
        for employee in self.employees:
            employee.do_action()

        if not self.action_to_do:
            return

        if self.action_to_do[0] == "SELL":
            field, nb_days_off = self.action_to_do[1:]
            if nb_days_off:
                self.action_to_do = ("SELL", field, nb_days_off - 1)
            else:
                if field.needed_water or not field.content:
                    pass  # cancel sell
                else:
                    print("money before", self.money)
                    self.money += self.game.field_price(field)
                    print("money after", self.money)
                    field.content = Vegetable.NONE

                self.action_to_do = tuple()

    def add_action(self: "Farm", action: str) -> None:
        if self.blocked:
            return
        print("###", action)
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

    def _acheter_champ(self: "Farm", owner_id: str) -> None:
        if self.action_to_do:
            raise ValueError("The farm owner is already busy")
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

        if employee.action_to_do:
            raise ValueError(f"Employee {employee_id} is already busy.")
        if not field.bought:
            raise ValueError(f"Field {field} is not already bought.")

        employee.action_to_do = ("SOW", vegetable, field)

    def _arroser(self: "Farm", employee_id: str, location_id: str) -> None:
        employee = self.get_employee(int(employee_id))
        field = self.get_field(int(location_id))

        if employee.action_to_do:
            raise ValueError(f"Employee {employee_id} is already busy.")
        if not field.bought:
            raise ValueError(f"Field {field} is not already bought.")

        employee.action_to_do = ("WATER", field)

    def _acheter_tracteur(self: "Farm", owner_id: str) -> None:
        if self.action_to_do:
            raise ValueError("The farm owner is already busy")
        if self.money < TRACTOR_PRICE:
            raise ValueError("Not enough money to buy tractor.")
        self.money -= TRACTOR_PRICE
        self.tractors.append(Tractor(id=self.next_tractor_id))
        self.next_tractor_id += 1

    def _vendre(self: "Farm", owner_id: str, location_id: str) -> None:
        if self.action_to_do:
            raise ValueError("The farm owner is already busy")
        field = self.get_field(int(location_id))
        if not field.bought:
            raise ValueError(f"Field {field} is not already bought.")
        if not field.content:
            raise ValueError(f"Field {field} does not contain vegetables.")
        if field.needed_water:
            raise ValueError(f"Field {field} needs more water.")

        self.action_to_do = ("SELL", field, NB_DAYS_TO_HARVEST)

    def _stocker(
        self: "Farm", employee_id: str, location_id: str, tractor_id: str
    ) -> None:
        employee = self.get_employee(int(employee_id))
        field = self.get_field(int(location_id))
        tractor = self.get_tractor(int(tractor_id))
        if employee.action_to_do:
            raise ValueError(f"Employee {employee_id} is already busy.")
        if not field.bought:
            raise ValueError(f"Field {field} is not already bought.")
        if not field.content:
            raise ValueError(f"Field {field} does not contain vegetables.")
        if field.needed_water:
            raise ValueError(f"Field {field} needs more water.")
        if (
            any(empl.tractor == tractor for empl in self.employees)
            and employee.tractor != tractor
        ):
            raise ValueError(f"Tractor {tractor_id} is already used.")

        step = 0
        employee.action_to_do = ("STOCK", field, tractor, step)

    def _cuisiner(self: "Farm", employee_id: str) -> None:
        employee = self.get_employee(int(employee_id))
        if employee.action_to_do:
            raise ValueError(f"Employee {employee_id} is already busy.")
        employee.action_to_do = ("COOK",)

    def _employer(self: "Farm", owner_id: str) -> None:
        if self.action_to_do:
            raise ValueError("The farm owner is already busy")
        self.employees.append(Employee(farm=self, id=self.next_employee_id))
        self.next_employee_id += 1

    def __repr__(self: "Farm") -> str:
        return f"Farm(name={self.name}, blocked={self.blocked}, money={self.money})"
