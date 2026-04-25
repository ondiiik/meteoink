from json import dumps, loads
from socket import socket


class Rpc:
    def __init__(self, s: socket) -> None:
        self._s = s

    def call(self, msg: dict[str, any]) -> dict[str, any]:
        self._s.send(dumps(msg))

        r = self._rcv_id(msg["id"])
        if "status" not in r:
            raise ValueError(
                f"Received malformed confirm message - missing 'status': {r}"
            )
        if r["status"] != "OK":
            raise ValueError(
                f"Received ERROR confirmation - detail: {r.get('detail', 'No details ...')}"
            )

        return r

    def call_bin(self, msg: dict[str, any]) -> bytes:
        self._s.send(dumps(msg))
        r = bytearray()
        while len(r) < msg["size"]:
            r += self._rcv()
        return r

    def _rcv_id(self, mid: str) -> dict[str, any]:
        m = self._rcv()
        try:
            r = loads(m)
        except ValueError as e:
            raise ValueError(f"Received malformed message: {m} - Detail: {e}")

        if "id" not in r:
            raise ValueError(f"Received malformed message - missing 'id': {r}")
        if r["id"] != mid:
            raise ValueError(
                f"Received wrong message id - expected '{mid}' but got '{r['id']}': {r}"
            )

        return r

    def _rcv(self) -> bytes:
        m = self._s.recv(4096)
        if not m:
            raise RuntimeError(f"Connection closed by server!")
        return m


__all__ = ("Rpc",)
