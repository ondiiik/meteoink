from sys import modules
from os import mkdir
from ujson import load, dump
from ubinascii import hexlify


class Json(dict):
    def __init__(self, file_name: str, default: dict):
        self.file_name = file_name

        try:
            with open(file_name, "r") as f:
                super().__init__(load(f))
        except:
            super().__init__(default if isinstance(default, dict) else default())
            self.flush()

    def flush(self) -> None:
        try:
            with open(self.file_name, "r") as f:
                before = load(f)
        except:
            before = dict()

        if before != self:
            with open(self.file_name, "w") as f:
                dump(self, f)
