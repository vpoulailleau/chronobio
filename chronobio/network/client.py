import argparse
from socket import AF_INET, SOCK_STREAM, socket

from .data_handler import DataHandler


class Client:
    def __init__(
        self, server_addr: str, port: int, username: str, spectator: bool
    ) -> None:
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((server_addr, port))
        self._data_handler = DataHandler(sock)

        self.send(f"{int(spectator)}\n")
        self.send(f"{username}\n")

        line = self._data_handler.readline()
        if line == "OK":
            pass  # successful connection
        else:
            raise ConnectionRefusedError("Connection refused by server", line)

    def send(self, message: str) -> None:
        self._data_handler.write(message)

    def read_json(self) -> object:
        """TODO."""


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
    parser.add_argument(
        "-u",
        "--user",
        type=str,
        help="name of the user",
        default="unknown",
        required=True,
    )
    args = parser.parse_args()

    client = Client(args.address, args.port, args.user, spectator=False)
