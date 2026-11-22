# Encrypted channel over TCP socket (used for remote display)
#
# Both sides share 256-bit key (`behavior["display_key"]` on meteostation, stored
# on server for each station under its unique ID). Module works in MicroPython
# (`cryptolib`, HW accelerated AES on ESP32) and in PC Python, so it can be used
# also as reference implementation for server side (`SecureSocket.server`).
#
# Protocol
# ========
#
# 1. Handshake (plain text):
#
#       client -> server:  b"MINK" | version (1B) | Nc (16B random) | len(id) (1B) | id
#       server -> client:  b"MINK" | version (1B) | Ns (16B random)
#
#    `id` is station unique ID (`machine.unique_id()`), so server can select the key.
#
# 2. Session keys (separate for each direction, `dir` is b"c2s" or b"s2c"):
#
#       transcript = SHA256(client handshake bytes | server handshake bytes)
#       material(what) = SHA256(key | dir | what | transcript)
#       aes key = material(b" key"), CBC IV = material(b" iv")[:16],
#       mac key = material(b" mac")
#
# 3. Each message is sent as one frame:
#
#       length (4B, big endian) | ciphertext (length bytes) | tag (16B)
#
#    Length is limited by receiver (`max_frame`) as it is used for buffer
#    allocation before frame is authenticated.
#
#    ciphertext = AES-256-CBC(PKCS#7 padded message). CBC chain continues from
#    frame to frame for the whole connection (one chain per direction).
#    tag = HMAC-SHA256(mac key, seq (8B, big endian) | length | ciphertext)[:16],
#    where `seq` counts frames in given direction from 0.
#
#    Frame with wrong tag means wrong key or tampered data and connection
#    has to be closed.
from hashlib import sha256
from os import urandom
from struct import pack, unpack
from cryptolib import aes
from micropython import const


_MAGIC = b"MINK"
_VERSION = const(2)
_NONCE_LEN = const(16)
_TAG_LEN = const(16)
_MODE_CBC = const(2)
_MAX_FRAME = const(64 * 1024)  # Default limit of received message (enough for JSON messages)


class SecureError(ValueError): ...


def _equal(a, b) -> bool:
    if len(a) != len(b):
        return False
    r = 0
    for x, y in zip(a, b):
        r |= x ^ y
    return r == 0


class _Direction:
    def __init__(self, key, label, encrypt, transcript):
        def material(what):
            return sha256(key + label + what + transcript).digest()

        cipher = aes(material(b" key"), _MODE_CBC, material(b" iv")[:16])
        self.process = cipher.encrypt if encrypt else cipher.decrypt

        mac = material(b" mac") + bytes(32)
        self._ipad = bytes(b ^ 0x36 for b in mac)
        self._opad = bytes(b ^ 0x5C for b in mac)
        self._seq = 0

    def tag(self, hdr, data) -> bytes:
        inner = sha256(self._ipad)
        inner.update(pack(">Q", self._seq))
        inner.update(hdr)
        inner.update(data)
        self._seq += 1
        return sha256(self._opad + inner.digest()).digest()[:_TAG_LEN]


class SecureSocket:
    """Encrypted message channel over connected socket

    Use `SecureSocket.client` or `SecureSocket.server` to establish it.
    """

    def __init__(self, sock, key, hello_c, hello_s, client, max_frame):
        if len(key) != 32:
            raise SecureError("Key has to be 32 bytes long")

        self._s = sock
        self._readinto = _readinto_of(sock)
        self._max_frame = max_frame

        # Keys depend on whole handshake, so any its modification is detected
        transcript = sha256(hello_c + hello_s).digest()
        tx, rx = (b"c2s", b"s2c") if client else (b"s2c", b"c2s")
        self._tx = _Direction(key, tx, True, transcript)
        self._rx = _Direction(key, rx, False, transcript)

    @classmethod
    def client(cls, sock, key: bytes, ident: bytes, max_frame: int = _MAX_FRAME) -> "SecureSocket":
        """Establish channel from client (meteostation) side

        :param sock:       Connected socket.
        :param key:        Shared 32 bytes key.
        :param ident:      Station identifier (max 255 bytes) used by server for key selection.
        :param max_frame:  Maximal size of received message (e.g. size of display frame buffer).
        """
        hello_c = _MAGIC + bytes((_VERSION,)) + urandom(_NONCE_LEN) + bytes((len(ident),)) + ident
        sock.sendall(hello_c)

        hello_s = bytes(_read(_readinto_of(sock), len(_MAGIC) + 1 + _NONCE_LEN))
        if hello_s[: len(_MAGIC)] != _MAGIC or hello_s[len(_MAGIC)] != _VERSION:
            raise SecureError("Server does not support this version of encrypted channel")

        return cls(sock, key, hello_c, hello_s, True, max_frame)

    @classmethod
    def server(cls, sock, key_lookup, max_frame: int = _MAX_FRAME) -> "SecureSocket":
        """Establish channel from server side

        :param sock:        Accepted socket.
        :param key_lookup:  Callable returning 32 bytes key for station ID (bytes),
                            or `None` for unknown station.
        :param max_frame:   Maximal size of received message.
        """
        readinto = _readinto_of(sock)
        r = bytes(_read(readinto, len(_MAGIC) + 1 + _NONCE_LEN + 1))
        if r[: len(_MAGIC)] != _MAGIC or r[len(_MAGIC)] != _VERSION:
            raise SecureError("Client does not support this version of encrypted channel")

        ident = bytes(_read(readinto, r[-1]))
        hello_c = r + ident
        key = key_lookup(ident)
        if key is None:
            raise SecureError(f"Unknown station {ident.hex()}")

        hello_s = _MAGIC + bytes((_VERSION,)) + urandom(_NONCE_LEN)
        sock.sendall(hello_s)

        return cls(sock, key, hello_c, hello_s, False, max_frame)

    def send(self, data) -> None:
        """Send one message"""
        l = len(data)
        pad = 16 - l % 16
        buf = bytearray(l + pad)
        buf[:l] = data
        buf[l:] = bytes((pad,)) * pad
        self._tx.process(buf, buf)

        hdr = pack(">I", len(buf))
        self._s.sendall(hdr)
        self._s.sendall(buf)
        self._s.sendall(self._tx.tag(hdr, buf))

    def recv(self) -> memoryview:
        """Receive one message"""
        hdr = self._read(4)
        n = unpack(">I", hdr)[0]
        if n == 0 or n % 16 or n > self._max_frame + 16:  # + padding
            raise SecureError(f"Invalid frame length {n}")

        buf = self._read(n)
        tag = self._read(_TAG_LEN)
        if not _equal(tag, self._rx.tag(hdr, buf)):
            raise SecureError("Frame authentication failed (wrong display key?)")

        self._rx.process(buf, buf)
        pad = buf[-1]
        if not 0 < pad <= 16:
            raise SecureError("Invalid padding")

        return memoryview(buf)[: n - pad]

    def close(self) -> None:
        self._s.close()

    def _read(self, n) -> bytearray:
        return _read(self._readinto, n)


def _readinto_of(sock):
    try:
        return sock.recv_into  # PC Python
    except AttributeError:
        return sock.readinto  # MicroPython


def _read(readinto, n) -> bytearray:
    buf = bytearray(n)
    mv = memoryview(buf)
    got = 0
    while got < n:
        cnt = readinto(mv[got:])
        if not cnt:
            raise RuntimeError("Connection closed by peer!")
        got += cnt
    return buf
