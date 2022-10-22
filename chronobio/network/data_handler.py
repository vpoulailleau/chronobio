import json
from socket import socket
from threading import Lock, Thread
from time import sleep


class DataHandler:
    BUFSIZ = 1024

    def _receive_data(self) -> None:
        while True:
            try:
                data = self.socket.recv(self.BUFSIZ)
            except (BrokenPipeError, OSError):
                return
            with self._input_lock:
                self._inputbytes += data
                try:
                    self._input += self._inputbytes.decode("utf-8")
                    self._inputbytes = b""
                except UnicodeDecodeError:
                    pass

    def __init__(self, socket: socket):
        self._inputbytes = b""
        self._input = ""
        self._input_lock = Lock()
        self.socket = socket

        receive_thread = Thread(target=self._receive_data, args=())
        receive_thread.start()

    def readline(self) -> str:
        while "\n" not in self._input:
            sleep(0.01)
        with self._input_lock:
            index = self._input.index("\n")
            line = self._input[:index]
            self._input = self._input[index + 1 :]
            return line

    def read_json(self) -> object:
        json_text = ""
        while True:
            json_text += "\n" + self.readline()
            try:
                return json.loads(json_text)
            except json.JSONDecodeError:
                pass  # not yet a full JSON object

    def write(self, message: str) -> None:
        self.socket.send(bytes(message, "utf8"))

    def write_json(self, data: object) -> None:
        self.write(json.dumps(data))
