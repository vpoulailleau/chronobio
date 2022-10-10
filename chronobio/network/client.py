import argparse
from socket import AF_INET, SOCK_STREAM, socket


class Client:
    def __init__(
        self, server_addr: str, port: int, username: str, spectator: bool
    ) -> None:
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect((server_addr, port))

        self.socket.send(bytes(str(int(spectator)), encoding="utf-8"))
        self.socket.send(bytes(username, encoding="utf8"))

    def receive(self, callback) -> None:
        """Reception of messages."""
        try:
            # TODO gérer des longs messages
            msg = self.socket.recv(4096).decode("utf8")
            callback(msg)
        except OSError:
            break

    def send(self, message: str) -> None:
        self.socket.send(bytes(message, "utf8"))


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
        default=33000,
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

    client = Client(args.address, args.port, args.user, False)
    client.send("Coucou")
    client.receive(print)
