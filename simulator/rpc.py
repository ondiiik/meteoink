from json import dumps, loads


class Rpc:
    """JSON RPC over message channel (`secsock.SecureSocket`)"""

    def __init__(self, s: "SecureSocket") -> None:
        self._s = s

    def call(self, msg: dict[str, any]) -> dict[str, any]:
        self._s.send(dumps(msg).encode())

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

    def call_bin(self, msg: dict[str, any]) -> memoryview:
        self._s.send(dumps(msg).encode())
        r = self._s.recv()
        if len(r) != msg["size"]:
            raise ValueError(
                f"Received {len(r)} bytes of binary data, but {msg['size']} expected"
            )
        return r

    def _rcv_id(self, mid: str) -> dict[str, any]:
        m = bytes(self._s.recv())
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
