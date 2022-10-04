import math

from chronobio.game.constants import CLIMATE_DISASTER_THRESHOLD
from chronobio.game.game import Game

game = Game()
game.add_player("Vincent")
game.add_player("Benjamin")

farm = game.farms[0]
farm.add_action("0 EMPRUNTER 100000")
farm.add_action("0 ACHETER_CHAMP")
farm.add_action("0 ACHETER_CHAMP")
farm.add_action("0 ACHETER_CHAMP")
farm.add_action("0 ACHETER_TRACTEUR")
farm.add_action("0 ACHETER_TRACTEUR")
farm.add_action("0 EMPLOYER")
farm.add_action("0 EMPLOYER")
farm.add_action("1 SEMER PATATE 3")
print(farm)

for day in range(20 * 360):
    game.new_day()

    farm = game.farms[0]
    field = farm.fields[2]
    if field.content and not field.needed_water and not farm.action_to_do:
        # farm.add_action("0 VENDRE 3")
        if farm.employees and not farm.employees[0].action_to_do:
            farm.add_action("1 STOCKER 3 1")
    elif farm.employees and not farm.employees[0].action_to_do:
        if field.content:
            farm.add_action("1 ARROSER 3")
        else:
            farm.add_action("1 SEMER PATATE 3")
    if len(farm.employees) > 1 and not farm.employees[1].action_to_do:
        if sum(farm.soup_factory.stock.values()):
            farm.add_action("2 CUISINER")
    if day == 1000:
        farm.add_action("0 LICENCIER 2")

    print("New day", game.date)
    value = math.log(game.greenhouse_gas + 1, 2)
    no_risk = min(value, CLIMATE_DISASTER_THRESHOLD)
    risk = max(0, value - CLIMATE_DISASTER_THRESHOLD)
    percent = 100 * risk / (risk + no_risk)

    print(f" - Greenhouse gas: {game.greenhouse_gas} => {percent}%")

    for farm in game.farms:
        if farm.name:
            print(f" - {farm.name}: {farm.score}")
            print("  ", farm.tractors)
            print("  ", farm.employees)
            print("  ", farm.fields)
            print("  ", farm.soup_factory.stock)
