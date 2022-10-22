import argparse
import json
from pprint import pprint
from time import sleep

from chronobio.game.constants import MAX_NB_PLAYERS, SERVER_CONNECTION_TIMEOUT
from chronobio.game.game import Game
from chronobio.network.server import Server


class GameServer(Server):
    def __init__(self: "GameServer", host: str, port: int):
        super().__init__(host, port)
        self.game = Game()

    @property
    def players(self):
        return [client for client in self.clients if not client.spectator]

    def _turn(self: "GameServer"):
        self.game.new_day()
        state = self.game.state()
        print("Sending current state")
        pprint(state)
        state_json = json.dumps(state) + "\n"
        for client in self.clients:
            client.network.write(state_json)

        for player in self.players:
            print("Waiting commands from", player)
            commands = player.network.read_json()  # TODO ajouter un timeout
            print(commands)
            for farm in self.game.farms:
                if farm.name == player.name:
                    player_farm = farm
                    break
            else:
                raise ValueError(f"Farm is not found ({player.name})")

            for command in commands["commands"]:
                player_farm.add_action(command)

    def run(self: "GameServer") -> None:
        while not self.players:
            print("Waiting for player clients")
            sleep(1)

        for second in range(1, SERVER_CONNECTION_TIMEOUT + 1):
            print(f"Waiting other players ({second}/{SERVER_CONNECTION_TIMEOUT})")
            if len(self.players) == MAX_NB_PLAYERS:
                break
            sleep(1)

        for player_name in {player.name for player in self.players}:
            self.game.add_player(player_name)
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
