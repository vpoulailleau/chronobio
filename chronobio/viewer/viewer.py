import logging
from threading import Thread
from time import sleep
from typing import NoReturn

from chronobio.game.exceptions import ChronobioNetworkError
from chronobio.network.client import Client
from chronobio.viewer.window import input_queue, gui_thread


def network_thread(server_addr: str, server_port: int) -> None:
    client = Client(server_addr, server_port, spectator=True)
    while True:
        try:
            data = client.read_json()
            input_queue.put(data)
        except ChronobioNetworkError:
            logging.exception("End of network communication")
            break
    for _ in range(6):
        sleep(10)
        logging.info("sleeping")


class Viewer:
    def __init__(self, server_addr: str, port: int) -> None:
        logging.info("Start network")
        Thread(target=network_thread, daemon=True, args=[server_addr, port]).start()
        logging.info("Start GUI")
        gui_thread()
