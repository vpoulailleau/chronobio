from __future__ import annotations

import re
import typing

from chronobio.game.constants import (
    FARM_MONEY_PER_DAY,
    FIELD_MONEY_PER_DAY,
    FIELD_PRICE,
    GREENHOUSE_GAS_PER_TRACTOR,
    MAX_NB_EMPLOYEES,
    MAX_NB_LOANS,
    MAX_NB_TRACTORS,
    NB_DAYS_TO_HARVEST,
    TRACTOR_PRICE,
)
from chronobio.game.employee import Employee
from chronobio.game.field import Field
from chronobio.game.loan import Loan
from chronobio.game.location import fields
from chronobio.game.soup_factory import SoupFactory
from chronobio.game.tractor import Tractor
from chronobio.game.vegetable import Vegetable

if typing.TYPE_CHECKING:
    from chronobio.game.game import Game


class Farm:
    def __init__(self: "Farm", game: Game, index: int) -> None:
        self.game = game
        self.index = index
        self.blocked: bool = True
        self.name: str = ""
        self.money: float = 100_000
        self.fields: list[Field] = [Field(location) for location in fields]
        self.tractors: list[Tractor] = []
        self.loans: list[Loan] = []
        self.soup_factory: SoupFactory = SoupFactory()
        self.employees: list[Employee] = []
        self.next_employee_id: int = 1
        self.next_tractor_id: int = 1
        self.action_to_do: tuple = ()
        self.event_messages = []

    def invalid_action(self: "Farm", message: str) -> None:
        self.event_messages.append(f"[INVALID_ACTION] {message}")
        if "Employee" in message and "busy" in message:
            employee_id = int(message.split()[1])
            for employee in self.employees:
                if employee.id != employee_id:
                    continue
                self.event_messages.append(
                    f"Employee was doing: {employee.action_to_do}"
                )
                break
        self.blocked = True

    def income(self: "Farm") -> None:
        if self.blocked:
            return

        self.money += FARM_MONEY_PER_DAY
        for field in self.fields:
            if field.content != Vegetable.NONE:
                self.money += FIELD_MONEY_PER_DAY

    def expend(self: "Farm", day: int) -> None:
        if self.blocked:
            return

        if day % 30 == 0 and day != 0:
            for employee in self.employees:
                if self.money < employee.salary:
                    self.invalid_action(
                        f"Not enough money to pay employee {employee.id}."
                    )
                    return
                self.money -= employee.salary
                employee.raise_salary()

            for loan in self.loans:
                cost = loan.month_cost(self.game.day)
                if self.money < cost:
                    self.invalid_action(f"Not enough money to pay loan {loan}.")
                    return
                self.money -= cost

    def pollute(self: "Farm") -> None:
        if not self.blocked:
            self.game.greenhouse_gas += len(self.tractors) * GREENHOUSE_GAS_PER_TRACTOR

    def get_employee(self: "Farm", employee_id: int) -> Employee:
        for em in self.employees:
            if employee_id == em.id:
                employee = em
                break
        else:
            employee = None
        if employee is None:
            self.invalid_action(f"No employee with ID: {employee_id}.")
        return employee

    def get_field(self: "Farm", location_id: int) -> Field:
        if not (1 <= location_id <= 5):
            self.invalid_action(f"Invalid field ID: {location_id}.")
            return None
        return self.fields[location_id - 1]

    def get_tractor(self: "Farm", tractor_id: int) -> Tractor:
        for tr in self.tractors:
            if tractor_id == tr.id:
                tractor = tr
                break
        else:
            tractor = None
        if tractor is None:
            self.invalid_action(f"No tractor with ID: {tractor_id}.")
        return tractor

    def get_vegetable(self: "Farm", vegetable_name: str) -> Vegetable:
        translations = {
            "PATATE": "POTATO",
            "POIREAU": "LEEK",
            "TOMATE": "TOMATO",
            "OIGNON": "ONION",
            "COURGETTE": "ZUCCHINI",
        }
        vegetable_enum = translations.get(vegetable_name)
        if vegetable_enum is None:
            self.invalid_action(f"Unknown vegetable: {vegetable_name}.")
            return None
        return Vegetable.__members__[vegetable_enum]

    def do_actions(self: "Farm") -> None:
        if self.blocked:
            return

        # logging.error("do actions %s", self.name)

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
                    # print("money before", self.money)
                    self.money += self.game.field_price(field)
                    # print("money after", self.money)
                    field.content = Vegetable.NONE

                self.action_to_do = ()

    def add_action(self: "Farm", action: str) -> None:
        if self.blocked:
            return

        vegetable_regex = "(PATATE|POIREAU|TOMATE|OIGNON|COURGETTE)"
        field_regex = "[1-5]"
        tractor_regex = r"\d+"
        person_regex = r"\d+"
        if not (
            re.search(
                rf"^{person_regex} (ACHETER_CHAMP|ACHETER_TRACTEUR|CUISINER|EMPLOYER)$",
                action,
            )
            or re.search(rf"^{person_regex} (ARROSER|VENDRE) {field_regex}$", action)
            or re.search(rf"^{person_regex} EMPRUNTER \d+$", action)
            or re.search(rf"^{person_regex} LICENCIER {person_regex}$", action)
            or re.search(
                rf"^{person_regex} SEMER {vegetable_regex} {field_regex}$", action
            )
            or re.search(
                rf"^{person_regex} STOCKER {field_regex} {tractor_regex}$", action
            )
        ):
            self.invalid_action(f"Unrecognized action format ({action}).")
            return

        parts = action.split()
        verb = parts.pop(1)
        getattr(self, "_" + verb.lower())(*parts)

    def _acheter_champ(self: "Farm", owner_id: str) -> None:
        if self.action_to_do:
            self.invalid_action("The farm owner is already busy")
        if owner_id != "0":
            self.invalid_action("This action is only valid for the farm owner.")
        for field in self.fields:
            if not field.bought:
                if self.money >= FIELD_PRICE:
                    field.bought = True
                    self.money -= FIELD_PRICE
                else:
                    self.invalid_action("Not enough money to buy field.")
                return
        self.invalid_action("Not enough money to buy field.")

    def _semer(
        self: "Farm", employee_id: str, vegetable_name: str, location_id: str
    ) -> None:
        employee = self.get_employee(int(employee_id))
        field = self.get_field(int(location_id))
        vegetable = self.get_vegetable(vegetable_name)
        if self.blocked:
            return

        if employee.action_to_do:
            self.invalid_action(f"Employee {employee_id} is already busy.")
        if not field.bought:
            self.invalid_action(f"Field {field} is not already bought.")

        if not self.blocked:
            employee.action_to_do = ("SOW", vegetable, field)

    def _arroser(self: "Farm", employee_id: str, location_id: str) -> None:
        employee = self.get_employee(int(employee_id))
        field = self.get_field(int(location_id))
        if self.blocked:
            return

        if employee.action_to_do:
            self.invalid_action(f"Employee {employee_id} is already busy.")
        if not field.bought:
            self.invalid_action(f"Field {field} is not already bought.")

        if not self.blocked:
            employee.action_to_do = ("WATER", field)

    def _acheter_tracteur(self: "Farm", owner_id: str) -> None:
        if self.action_to_do:
            self.invalid_action("The farm owner is already busy")
        if owner_id != "0":
            self.invalid_action("This action is only valid for the farm owner.")
        if self.money < TRACTOR_PRICE:
            self.invalid_action("Not enough money to buy tractor.")
        if self.next_tractor_id > MAX_NB_TRACTORS:
            self.invalid_action(
                f"Maximum number of tractors reached ({MAX_NB_TRACTORS}).",
            )
        if not self.blocked:
            self.money -= TRACTOR_PRICE
            self.tractors.append(Tractor(id_=self.next_tractor_id))
            self.next_tractor_id += 1

    def _vendre(self: "Farm", owner_id: str, location_id: str) -> None:
        if self.action_to_do:
            self.invalid_action("The farm owner is already busy")
        if owner_id != "0":
            self.invalid_action("This action is only valid for the farm owner.")
        field = self.get_field(int(location_id))
        if self.blocked:
            return

        if not field.bought:
            self.invalid_action(f"Field {field} is not already bought.")
        if not field.content:
            self.invalid_action(f"Field {field} does not contain vegetables.")
        if field.needed_water:
            self.invalid_action(f"Field {field} needs more water.")

        if not self.blocked:
            self.action_to_do = ("SELL", field, NB_DAYS_TO_HARVEST)

    def _stocker(
        self: "Farm", employee_id: str, location_id: str, tractor_id: str
    ) -> None:
        employee = self.get_employee(int(employee_id))
        field = self.get_field(int(location_id))
        tractor = self.get_tractor(int(tractor_id))
        if self.blocked:
            return

        if employee.action_to_do:
            self.invalid_action(f"Employee {employee_id} is already busy.")
        if not field.bought:
            self.invalid_action(f"Field {field} is not already bought.")
        if not field.content:
            self.invalid_action(f"Field {field} does not contain vegetables.")
        if field.needed_water:
            self.invalid_action(f"Field {field} needs more water.")
        if any(empl.tractor == tractor and empl != employee for empl in self.employees):
            self.invalid_action(f"Tractor {tractor_id} is already used.")

        if not self.blocked:
            step = 0
            employee.action_to_do = ("STOCK", field, tractor, step)

    def _cuisiner(self: "Farm", employee_id: str) -> None:
        employee = self.get_employee(int(employee_id))
        if self.blocked:
            return

        if employee.action_to_do:
            self.invalid_action(f"Employee {employee_id} is already busy.")

        if not self.blocked:
            employee.action_to_do = ("COOK",)

    def _employer(self: "Farm", owner_id: str) -> None:
        if self.action_to_do:
            self.invalid_action("The farm owner is already busy")
        if owner_id != "0":
            self.invalid_action("This action is only valid for the farm owner.")
        if self.next_employee_id > MAX_NB_EMPLOYEES:
            self.invalid_action(
                f"Maximum number of employees reached ({MAX_NB_EMPLOYEES})."
            )

        if not self.blocked:
            self.employees.append(Employee(farm=self, id_=self.next_employee_id))
            self.next_employee_id += 1

    def _licencier(self: "Farm", owner_id: str, employee_id: str) -> None:
        if self.action_to_do:
            self.invalid_action("The farm owner is already busy")
        if owner_id != "0":
            self.invalid_action("This action is only valid for the farm owner.")
        employee = self.get_employee(int(employee_id))
        if self.blocked:
            return

        self.employees.remove(employee)
        self.money -= employee.salary  # indemnity
        day = self.game.date[2]
        self.money -= employee.salary * day // 30  # salary
        if self.money < 0:
            self.invalid_action(f"Not enough money to fire {employee}")

    def _emprunter(self: "Farm", owner_id: str, amount_str: str) -> None:
        if self.action_to_do:
            self.invalid_action("The farm owner is already busy")
        if owner_id != "0":
            self.invalid_action("This action is only valid for the farm owner.")
        amount = int(amount_str)
        if amount < 0:
            self.invalid_action("The amount of the loan must be positive")
        elif amount > 1_000_000_000:
            self.invalid_action(
                "The amount of the loan must be less than 1 000 000 000",
            )
        if len(self.loans) > MAX_NB_LOANS:
            self.invalid_action(f"Maximum number of loans reached ({MAX_NB_LOANS}).")

        if not self.blocked:
            self.loans.append(Loan(amount, start_day=self.game.day))
            self.money += amount

    @property
    def score(self: "Farm") -> float:  # noqa: FNE007
        return self.money - sum(
            # TODO ne pas considérer que les emprunts sont remboursés si la ferme est bloquée
            loan.remaining_cost(self.game.day)
            for loan in self.loans
        )

    def state(self: "Farm") -> dict:
        return {
            "blocked": self.blocked,
            "name": self.name,
            "money": int(self.money),
            "score": int(self.score),
            "fields": [field.state() for field in self.fields],
            "tractors": [tractor.state() for tractor in self.tractors],
            "loans": [loan.state() for loan in self.loans],
            "soup_factory": self.soup_factory.state(),
            "employees": [employee.state() for employee in self.employees],
            "events": self.event_messages,
        }

    def __repr__(self: "Farm") -> str:
        return f"Farm(name={self.name}, blocked={self.blocked}, money={self.money})"
