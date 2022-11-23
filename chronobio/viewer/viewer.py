import logging
from threading import Thread
from time import sleep
from typing import NoReturn

from chronobio.game.exceptions import ChronobioNetworkError
from chronobio.network.client import Client
from chronobio.viewer.window import Window, gui_thread


class Viewer(Client):
    def __init__(self: "Viewer", server_addr: str, port: int) -> None:
        super().__init__(server_addr, port, spectator=True)
        self.window = Window()
        self.gui_thread = Thread(
            target=gui_thread, args=(self.window,), daemon=True
        ).start()

    def run(self: "Viewer") -> NoReturn:
        while True:
            try:
                data = self.read_json()
                print(str(data))
                self.window.input_queue.put(data)
            except ChronobioNetworkError:
                logging.exception("End of network communication")
                break
        for _ in range(6):
            sleep(10)
            logging.info("sleeping")
