from threading import Thread
from typing import NoReturn

from chronobio.network.client import Client
from chronobio.viewer.window import Window, gui_thread


class Viewer(Client):
    def __init__(self: "Viewer", server_addr: str, port: int) -> None:
        super().__init__(server_addr, port, spectator=True)
        self.window = Window()
        self.gui_thread = Thread(target=gui_thread, args=(self.window,)).start()

    def run(self: "Viewer") -> NoReturn:
        while True:
            print(str(self.read_json()))
