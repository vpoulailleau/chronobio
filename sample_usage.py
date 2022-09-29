from chronobio.game.game import Game

game = Game()
game.add_player("Vincent")
game.add_player("Benjamin")

farm = game.farms[0]
farm.action("0 ACHETER_CHAMP")
farm.action("0 ACHETER_CHAMP")
farm.action("0 ACHETER_CHAMP")
farm.action("0 EMPLOYER")
farm.action("1 SEMER PATATE 1")

for _ in range(100):
    game.new_day()
    print("New day", game.date)
    print(f" - Greenhouse gas: {game.greenhouse_gas}")

    for farm in game.farms:
        if farm.name:
            print(f" - {farm.name}: {farm.score}")
            print("  ", farm.employees)
            print("  ", farm.fields)
