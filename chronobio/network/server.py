import argparse
from dataclasses import dataclass
from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread


@dataclass
class ClientData:
    spectator: bool
    name: str
    socket: socket

    def __eq__(self, other):
        if isinstance(other, ClientData):
            return self.socket == other.socket
        raise NotImplemented

    def __hash__(self):
        return id(self.socket)


class Server:
    BUFSIZ = 1024

    def __init__(self, host: str, port: int) -> None:
        self.clients: set[ClientData] = set()
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind((host, port))

        self.socket.listen(5)
        print("Waiting for connection...")
        accept_thread = Thread(target=self.accept_incoming_connections, args=())
        accept_thread.start()
        accept_thread.join()
        self.socket.close()

    def handle_client_connection(self, client_socket: socket):
        """Handle a single client socket connection."""
        name = "unknown"
        spectator = "unknown"
        try:
            spectator = client_socket.recv(self.BUFSIZ).decode("utf8").split("\0")[0]
            name = client_socket.recv(self.BUFSIZ).decode("utf8").split("\0")[0]
        except (BrokenPipeError, OSError):
            return

        if spectator == "1":
            client = ClientData(spectator=True, name=name, socket=client)
        else:
            client = ClientData(spectator=False, name=name, socket=client)
        self.clients.add(client)
        self.communicate_with_client(client)

    def communicate_with_client(self, client: ClientData) -> None:
        try:
            while True:
                msg = client.socket.recv(self.BUFSIZ)
                try:
                    msg_str = msg.decode("utf-8")
                    msg_str = msg_str.split("\0")[0].strip()
                    break
                except UnicodeDecodeError:
                    msg_str = "ah ?"
                msg = msg_str.encode("utf8")
            client.socket.close()
        except OSError:
            pass
        self.clients.remove(client)

    def accept_incoming_connections(self):
        """Set up handling for incoming clients."""
        while True:
            try:
                client, client_address = self.socket.accept()
                Thread(target=self.handle_client_connection, args=(client,)).start()
            except (BrokenPipeError, OSError):
                pass


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
        "-p", "--port", type=int, help="location where server listens", default=33000
    )
    args = parser.parse_args()

    Server(args.address, args.port)
