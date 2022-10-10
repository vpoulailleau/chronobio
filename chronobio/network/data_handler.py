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
        receive_thread.join()

    def readline(self) -> str:
        while "\n" not in self._input:
            sleep(0.01)
        with self._input_lock:
            line, *remaining = self._input.splitlines()
            self._input = "\n".join(remaining)
            print("DATA HANDLER readline", line)
            return line

    def write(self, message: str) -> None:
        self.socket.send(bytes(message, "utf8"))
