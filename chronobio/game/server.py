import argparse
import json

from chronobio.game.game import Game
from chronobio.network.server import Server


class GameServer(Server):
    def __init__(self: "GameServer", host: str, port: int):
        super().__init__(host, port)
        self.game = Game()

    def _turn(self: "GameServer"):
        self.game.new_day()
        state = json.dumps(self.game.state()) + "\n"
        print("Sending current state", state)
        for client in self.clients:
            client.network.write(state)

    def run(self: "GameServer") -> None:
        from time import sleep

        sleep(5)  # wait connection
        while True:
            print("New game turn", self.game.day + 1)
            self._turn()
            sleep(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Game server.")
    parser.add_argument(
        "-a",
        "--address",
        type=str,
        help="name of server on the network",
        default="localhost",
    )
    parser.add_argument(
        "-p", "--port", type=int, help="location where server listens", default=16210
    )
    args = parser.parse_args()

    GameServer(args.address, args.port).run()
