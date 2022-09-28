from chronobio.game.game import Game

game = Game()

for _ in range(100):
    print("New day")
    game.new_day()
