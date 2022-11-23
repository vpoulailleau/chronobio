import argparse
from dataclasses import dataclass
from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread
from typing import NoReturn

from .data_handler import DataHandler


@dataclass
class ClientData:
    spectator: bool
    name: str
    network: DataHandler

    def __eq__(self, other):
        if isinstance(other, ClientData):
            return self.network is other.network
        raise NotImplemented

    def __hash__(self):
        return id(self.network)


class Server:
    def __init__(self: "Server", host: str, port: int) -> None:
        self.clients: set[ClientData] = set()
        print("Waiting for connection...")
        accept_thread = Thread(
            target=self.accept_incoming_connections, args=(host, port), daemon=True
        )
        accept_thread.start()

    def accept_incoming_connections(self: "Server", host: str, port: int) -> NoReturn:
        """Set up handling for incoming clients."""
        sock = socket(AF_INET, SOCK_STREAM)
        sock.bind((host, port))
        sock.listen(5)

        while True:
            try:
                client_socket, _ = sock.accept()
                Thread(
                    target=self.handle_client_connection, args=(client_socket,)
                ).start()
            except (BrokenPipeError, OSError):
                pass

        self.sock.close()

    def handle_client_connection(self, client_socket: socket) -> None:
        """Handle a single client socket connection."""
        print("Connection of a new client", flush=True)
        data_handler = DataHandler(client_socket)
        spectator = data_handler.readline().strip() == "1"
        print(" - Spectator", spectator)
        name = data_handler.readline().strip()
        print(" - Name", name)
        client = ClientData(spectator=spectator, name=name, network=data_handler)
        self.clients.add(client)
        self.write(client, "OK\n")
        print(" - New client connected", client, flush=True)

    @staticmethod
    def write(client: ClientData, message: str) -> None:
        # assume client is connected
        client.network.write(message)


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

    Server(args.address, args.port)
