import argparse
import json
import logging
from time import sleep

from chronobio.game.constants import MAX_NB_PLAYERS, SERVER_CONNECTION_TIMEOUT
from chronobio.game.exceptions import ChronobioNetworkError
from chronobio.game.game import Game
from chronobio.network.server import Server


class GameServer(Server):
    def __init__(self: "GameServer", host: str, port: int, duration: int, fast: bool):
        super().__init__(host, port)
        self.game = Game()
        self.duration = duration
        self.fast = fast

    @property
    def players(self):
        return [client for client in self.clients if not client.spectator]

    def _turn(self: "GameServer"):  # TODO split in smaller methods
        self.game.new_day()
        state = self.game.state()
        logging.info("Sending current state")
        logging.debug(state)
        state_json = json.dumps(state) + "\n"
        for client in list(self.clients):
            logging.debug("sending to %s", client.name)
            try:
                client.network.write(state_json)
            except ChronobioNetworkError:
                logging.exception("Problem sending state to client")
                self.clients.remove(client)
                if not client.spectator:
                    for farm in self.game.farms:
                        if farm.name == client.name:
                            farm.blocked = True
        self.game.log_messages()
        self.game.clear_event_messages()

        for player in list(self.players):
            logging.info("Waiting commands from %s", player.name)
            try:
                commands = player.network.read_json(timeout=2)
            except ChronobioNetworkError:
                logging.exception("timeout")
                self.clients.remove(player)
                for farm in self.game.farms:
                    if farm.name == player.name:
                        farm.blocked = True
                continue

            logging.debug(commands)
            for farm in self.game.farms:
                if farm.name == player.name:
                    player_farm = farm
                    break
            else:
                raise ValueError(f"Farm is not found ({player.name})")

            for command in commands["commands"]:
                logging.info(command)
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
        for day in range(self.duration):
            logging.info("New game turn %d", day + 1)
            self._turn()
            if not self.fast:
                sleep(0.1)


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
    parser.add_argument(
        "-d",
        "--duration",
        type=int,
        help="number of simulation days",
        default=5 * 12 * 30,
    )
    parser.add_argument(
        "-f",
        "--fast",
        help="fast simulation",
        action="store_true",
    )

    args = parser.parse_args()

    logging.basicConfig(
        filename="server.log",
        encoding="utf-8",
        level=logging.INFO,
        format="%(asctime)s [%(levelname)-8s] %(filename)20s(%(lineno)3s):%(funcName)-20s :: %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
    )
    logging.info("Launching server")
    GameServer(args.address, args.port, args.duration, args.fast).run()
