from __future__ import annotations

import math
from contextlib import suppress
from importlib.resources import files

import arcade

from chronobio.game.location import Location
from chronobio.viewer.constants import constants

DEFAULT_TEXTURE = ":resources:images/tiles/boxCrate_double.png"

location_to_position: dict[Location, tuple[float, float]] = {
    Location.FARM: (
        constants.FARM_BUILDING_DISTANCE_FROM_CENTER,
        constants.FARM_BUILDING_WIDTH,
    ),
    Location.FIELD1: (
        constants.FIELD_OFFSET + 0 * constants.FIELD_DISTANCE,
        constants.FIELD_WIDTH + 30,
    ),
    Location.FIELD2: (
        constants.FIELD_OFFSET + 1 * constants.FIELD_DISTANCE,
        constants.FIELD_WIDTH + 30,
    ),
    Location.FIELD3: (
        constants.FIELD_OFFSET + 2 * constants.FIELD_DISTANCE,
        constants.FIELD_WIDTH + 30,
    ),
    Location.FIELD4: (
        constants.FIELD_OFFSET + 3 * constants.FIELD_DISTANCE,
        constants.FIELD_WIDTH + 30,
    ),
    Location.FIELD5: (
        constants.FIELD_OFFSET + 4 * constants.FIELD_DISTANCE,
        constants.FIELD_WIDTH + 30,
    ),
    Location.SOUP_FACTORY: (
        constants.SOUP_FACTORY_DISTANCE_FROM_CENTER,
        constants.SOUP_FACTORY_WIDTH,
    ),
}

vegetable_to_sprite: dict[str, str] = {
    "NONE": files("chronobio.viewer").joinpath("images/transparent.png"),
    "POTATO": files("chronobio.viewer").joinpath("images/potato.png"),
    "LEEK": files("chronobio.viewer").joinpath("images/leek.png"),
    "TOMATO": files("chronobio.viewer").joinpath("images/tomato.png"),
    "ONION": files("chronobio.viewer").joinpath("images/onion.png"),
    "ZUCCHINI": files("chronobio.viewer").joinpath("images/zucchini.png"),
}


class MovingEntity:
    def __init__(self, sprite_path=DEFAULT_TEXTURE) -> None:
        self.target_location: Location = Location.FARM
        self.sprite: arcade.Sprite = arcade.Sprite(sprite_path, scale=1.0)
        self.sprite.width = 80
        self.sprite.height = 80
        self.sprite.angle = 0
        self.x, self.y = location_to_position[self.target_location]

    def update_position(self, farm: "Farm"):
        target_x, target_y = location_to_position[self.target_location]
        self.x = (target_x - self.x) * 0.2 + self.x
        self.y = (target_y - self.y) * 0.2 + self.y

        self.sprite.center_x, self.sprite.center_y = farm.rotate(self.x, self.y)


class Employee(MovingEntity):
    def __init__(self, sprite_path=DEFAULT_TEXTURE) -> None:
        super().__init__(sprite_path)
        self.id = 0

    def update_position(self, farm: "Farm"):
        target_x, target_y = location_to_position[self.target_location]
        target_x += (self.id % 12 - 6) * 5
        self.x = (target_x - self.x) * 0.2 + self.x
        self.y = (target_y - self.y) * 0.2 + self.y

        self.sprite.center_x, self.sprite.center_y = farm.rotate(self.x, self.y)


class ClimateEvent(MovingEntity):
    MAX_SIZE = int(150 / 1777 * constants.SCREEN_WIDTH)
    MIN_SIZE = int(30 / 1777 * constants.SCREEN_WIDTH)

    def __init__(self, sprite_path=DEFAULT_TEXTURE) -> None:
        super().__init__(sprite_path)
        self.size = self.MIN_SIZE

    def update_position(self, farm: "Farm"):
        self.x = location_to_position[self.target_location][0]
        self.y = 0
        self.size += 5
        self.sprite.width = self.size
        self.sprite.height = self.size
        self.sprite.alpha = max(
            0, int((self.MAX_SIZE - self.size) / (self.MAX_SIZE - self.MIN_SIZE) * 255)
        )

        self.sprite.center_x, self.sprite.center_y = farm.rotate(self.x, self.y)


class Vegetable(MovingEntity):
    def __init__(self, sprite_path=DEFAULT_TEXTURE) -> None:
        super().__init__(sprite_path)
        self.sprite_path = sprite_path
        self.update_size(0)

    def update_size(self, needed_water: int) -> None:
        needed_water = min(needed_water, 20)
        size = 20 - needed_water
        self.sprite.width = int(4 * size / 1777 * constants.SCREEN_WIDTH)
        self.sprite.height = int(4 * size / 1777 * constants.SCREEN_WIDTH)

    def location(self, location: Location, farm: "Farm") -> None:
        self.target_location = location
        self.x, _ = location_to_position[self.target_location]
        self.y = 0
        self.sprite.center_x, self.sprite.center_y = farm.rotate(self.x, self.y)


class Soup(MovingEntity):
    MAX_RADIUS = 100

    def __init__(self, angle: float, nb_vegetables: int) -> None:
        super().__init__(files("chronobio.viewer").joinpath("images/soup.png"))
        self.x, self.y = location_to_position[Location.SOUP_FACTORY]
        self.angle = angle
        self.radius = 0
        self.sprite.width = 20 * nb_vegetables
        self.sprite.height = 20 * nb_vegetables

    def update_position(self, farm: "Farm"):
        self.radius = (self.MAX_RADIUS - self.radius) * 0.2 + self.radius
        self.x = constants.SOUP_FACTORY_DISTANCE_FROM_CENTER + self.radius * math.cos(
            math.radians(self.angle)
        )
        self.y = self.radius * math.sin(math.radians(self.angle))

        self.sprite.center_x, self.sprite.center_y = farm.rotate(self.x, self.y)
        self.sprite.alpha = min(
            255, int((self.MAX_RADIUS - self.radius) / self.MAX_RADIUS * 1024)
        )


class Farm:
    def __init__(self, x, y, angle=0):
        self.angle = angle
        self.x = x
        self.y = y
        self.employees: dict[int, MovingEntity] = {}
        self.tractors: dict[int, MovingEntity] = {}
        self.vegetables: list[Vegetable] = []
        self.climate_events: list[ClimateEvent] = []
        self.soups: list[Soup] = []
        self.soup_angle = 0
        self.sprite_list = arcade.SpriteList()
        self.blocked = False
        self.blocked_sprite = arcade.Sprite(
            files("chronobio.viewer").joinpath("images/blocked.png"), scale=1.0
        )
        self.blocked_sprite.width = 300
        self.blocked_sprite.height = 300
        self.blocked_sprite.angle = 0
        self.blocked_sprite.center_x, self.blocked_sprite.center_y = self.rotate(
            location_to_position[Location.FIELD3][0], 0
        )
        self.closed = False
        self.closed_sprite = arcade.Sprite(
            files("chronobio.viewer").joinpath("images/closed.png"), scale=1.0
        )
        self.closed_sprite.width = 100
        self.closed_sprite.height = 100
        self.closed_sprite.angle = 0
        self.closed_sprite.center_x, self.closed_sprite.center_y = self.rotate(
            location_to_position[Location.SOUP_FACTORY][0], 0
        )
        self.employees_per_location: dict[str, int] = {}
        self.stock: dict[str, int] = {}

    def rotate(self, x, y):
        cos = math.cos(math.radians(self.angle))
        sin = math.sin(math.radians(self.angle))
        return cos * x - sin * y + self.x, sin * x + cos * y + self.y

    def _update_employees(self: "Farm", data: dict) -> None:
        self.stock = data["soup_factory"]["stock"]
        seen = set()
        self.employees_per_location.clear()
        for employee in data["employees"]:
            seen.add(employee["id"])
            if employee["id"] not in self.employees:
                employee_entity = Employee(
                    files("chronobio.viewer").joinpath("images/farmer.png")
                )
                employee_entity.id = int(employee["id"])
                employee_entity.sprite.width = 60
                employee_entity.sprite.height = 60
                self.sprite_list.append(employee_entity.sprite)
                self.employees[employee["id"]] = employee_entity
            self.employees_per_location[employee["location"]] = (
                1 + self.employees_per_location.get(employee["location"], 0)
            )
            self.employees[employee["id"]].target_location = Location[
                employee["location"]
            ]
        for employee_id in list(self.employees):
            if employee_id not in seen:
                employee = self.employees.pop(employee_id)
                self.sprite_list.remove(employee.sprite)

    def _update_tractors(self: "Farm", data: dict) -> None:
        seen = set()
        for tractor in data["tractors"]:
            seen.add(tractor["id"])
            if tractor["id"] not in self.tractors:
                tractor_entity = MovingEntity(
                    files("chronobio.viewer").joinpath("images/tractor.png")
                )
                tractor_entity.sprite.width = 60
                tractor_entity.sprite.height = 60
                self.sprite_list.append(tractor_entity.sprite)
                self.tractors[tractor["id"]] = tractor_entity
            self.tractors[tractor["id"]].target_location = Location[tractor["location"]]
        for tractor_id in list(self.tractors):
            if tractor_id not in seen:
                tractor = self.tractors.pop(tractor_id)
                self.sprite_list.remove(tractor.sprite)

    def _update_vegetables(self: "Farm", data: dict) -> None:
        for vegetable in self.vegetables:
            with suppress(KeyError, ValueError):
                self.sprite_list.remove(vegetable.sprite)
        self.vegetables.clear()
        for field in data["fields"]:
            vegetable = Vegetable(
                sprite_path=vegetable_to_sprite.get(field["content"], DEFAULT_TEXTURE)
            )
            vegetable.location(Location[field["location"]], farm=self)
            vegetable.update_size(field["needed_water"])
            self.vegetables.append(vegetable)
            if "/transparent.png" not in str(vegetable.sprite_path):
                self.sprite_list.append(vegetable.sprite)

    def _update_soup(self: "Farm", data: dict) -> None:
        for event in data["events"]:
            if "[SOUP]" in event:
                nb_vegetables = int(event.split()[1])
                soup = Soup(angle=self.soup_angle, nb_vegetables=nb_vegetables)
                self.soups.append(soup)
                self.soup_angle += 10
                self.sprite_list.append(soup.sprite)

    def update(self, data: dict):
        if data["blocked"]:
            self.blocked = True
        self.closed = bool(data["soup_factory"]["days_off"])

        self._update_employees(data)
        self._update_tractors(data)
        self._update_vegetables(data)
        self._update_soup(data)

    def update_climate(self, events: list[str]) -> None:
        for event in events:
            if "[CLIMATE]" in event:
                if "flood" in event:
                    climate_event = ClimateEvent(
                        files("chronobio.viewer").joinpath("images/drops.png")
                    )
                    climate_event.target_location = Location.SOUP_FACTORY
                elif "fire" in event:
                    location = event.split()[-1]
                    climate_event = ClimateEvent(
                        files("chronobio.viewer").joinpath("images/fire.png")
                    )
                    climate_event.target_location = Location[location]
                elif "frost" in event:
                    location = event.split()[-1]
                    climate_event = ClimateEvent(
                        files("chronobio.viewer").joinpath("images/frost.png")
                    )
                    climate_event.target_location = Location[location]
                elif "heat wave" in event:
                    location = event.split()[-1]
                    climate_event = ClimateEvent(
                        files("chronobio.viewer").joinpath("images/drought.png")
                    )
                    climate_event.target_location = Location[location]
                self.climate_events.append(climate_event)
                self.sprite_list.append(climate_event.sprite)

    def _draw_animate(self: "Farm") -> None:
        for tractor in self.tractors.values():
            tractor.update_position(self)

        for employee in self.employees.values():
            employee.update_position(self)

        for soup in self.soups.copy():
            soup.update_position(self)
            if soup.radius / soup.MAX_RADIUS > 0.9:
                self.soups.remove(soup)
                self.sprite_list.remove(soup.sprite)

        for climate_event in self.climate_events.copy():
            climate_event.update_position(self)
            if climate_event.size > climate_event.MAX_SIZE:
                self.climate_events.remove(climate_event)
                self.sprite_list.remove(climate_event.sprite)

    def draw(self):
        if self.blocked:
            arcade.draw_sprite(self.blocked_sprite)
        else:
            self._draw_animate()
            self.draw_stock()
            self.sprite_list.draw()

            if self.closed:
                arcade.draw_sprite(self.closed_sprite)

    def draw_stock(self):
        x, y = self.rotate(
            constants.SOUP_FACTORY_DISTANCE_FROM_CENTER
            - constants.SOUP_FACTORY_WIDTH // 2,
            -constants.SOUP_FACTORY_WIDTH // 2,
        )
        for index, stock in enumerate(self.stock.values()):
            width = min(int(stock / 2000), 100)
            arcade.draw_lbwh_rectangle_filled(
                left=x + 10,
                bottom=y - 7 * index + 5,
                width=width,
                height=5,
                color=constants.COLORS[2],
            )
