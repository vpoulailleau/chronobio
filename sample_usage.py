from chronobio.game.game import Game

game = Game()
game.add_player("Vincent")
game.add_player("Benjamin")

farm = game.farms[0]
farm.action("0 ACHETER_CHAMP")
farm.action("0 ACHETER_CHAMP")
farm.action("0 ACHETER_CHAMP")
farm.action("1 SEMER PATATE 1")

for _ in range(100):
    print("New day")
    print(f" - Greenhouse gas: {game.greenhouse_gas}")
    game.new_day()

    for farm in game.farms:
        if farm.name:
            print(f" - {farm.name}: {farm.score}")
