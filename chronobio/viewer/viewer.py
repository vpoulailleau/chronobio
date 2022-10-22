from chronobio.network.client import Client

from typing import NoReturn

class Viewer(Client):
    def __init__(self: "Viewer", server_addr: str, port: int) -> None:
        super().__init__(server_addr, port, spectator=True)

    def run(self: "Viewer") -> NoReturn:
        while True:
            print(str(self.read_json()))
            