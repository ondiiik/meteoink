from zlib import decompress
from io import BytesIO


class DeflateIO:
    def __init__(self, byte_stream: BytesIO) -> None:
        self._byte_stream = byte_stream

    def __enter__(self) -> "DeflateIO":
        self._byte_stream.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._byte_stream.__exit__(exc_type, exc_val, exc_tb)

    def read(self) -> bytes:
        return decompress(self._byte_stream.read())