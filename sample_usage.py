from chronobio.game.game import Game

game = Game()
game.add_player("Vincent")
game.add_player("Benjamin")

for _ in range(100):
    print("New day")
    game.new_day()
