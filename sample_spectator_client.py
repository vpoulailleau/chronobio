import argparse
from typing import NoReturn

from chronobio.network.client import Client


class SpectatorGameClient(Client):
    def __init__(self: "SpectatorGameClient", server_addr: str, port: int) -> None:
        super().__init__(server_addr, port, spectator=True)

    def run(self: "SpectatorGameClient") -> NoReturn:
        while True:
            print(str(self.read_json()))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Game client.")
    parser.add_argument(
        "-a",
        "--address",
        type=str,
        help="name of server on the network",
        default="localhost",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        help="location where server listens",
        default=16210,
    )
    args = parser.parse_args()

    SpectatorGameClient(args.address, args.port).run()
