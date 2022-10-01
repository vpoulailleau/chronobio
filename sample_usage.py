from chronobio.game.game import Game

game = Game()
game.add_player("Vincent")
game.add_player("Benjamin")

farm = game.farms[0]
farm.add_action("0 ACHETER_CHAMP")
farm.add_action("0 ACHETER_CHAMP")
farm.add_action("0 ACHETER_CHAMP")
farm.add_action("0 ACHETER_TRACTEUR")
farm.add_action("0 ACHETER_TRACTEUR")
farm.add_action("0 EMPLOYER")
farm.add_action("1 SEMER PATATE 3")
print(farm)

for _ in range(20):
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

    print("New day", game.date)
    print(f" - Greenhouse gas: {game.greenhouse_gas}")

    for farm in game.farms:
        if farm.name:
            print(f" - {farm.name}: {farm.score}")
            print("  ", farm.tractors)
            print("  ", farm.employees)
            print("  ", farm.fields)
            print("  ", farm.soup_factory.stock)
