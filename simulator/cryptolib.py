# MicroPython `cryptolib` adaptation for PC Python
#
# Provides `aes(key, mode, iv=None)` with ECB (1) and CBC (2) modes and the same
# behavior as MicroPython (one object either encrypts or decrypts, in place
# operation through `out_buf`). Uses `cryptography` package when installed,
# otherwise pure Python AES (slow, but sufficient for simulator).

MODE_ECB = 1
MODE_CBC = 2


# ---------------------------------------------------------------------------
# Pure Python AES block cipher (FIPS-197)
# ---------------------------------------------------------------------------
def _xtime(a):
    a <<= 1
    return (a ^ 0x11B) if a & 0x100 else a


def _mul(a, b):
    r = 0
    while b:
        if b & 1:
            r ^= a
        a = _xtime(a)
        b >>= 1
    return r


def _build_sbox():
    sbox = [0] * 256
    p = q = 1
    while True:
        p = p ^ _xtime(p)  # multiply p by 3
        q ^= q << 1  # divide q by 3
        q ^= q << 2
        q ^= q << 4
        q &= 0xFF
        if q & 0x80:
            q ^= 0x09
        x = q ^ (q << 1 | q >> 7) ^ (q << 2 | q >> 6) ^ (q << 3 | q >> 5) ^ (q << 4 | q >> 4)
        sbox[p] = (x ^ 0x63) & 0xFF
        if p == 1:
            break
    sbox[0] = 0x63
    inv = [0] * 256
    for i, v in enumerate(sbox):
        inv[v] = i
    return sbox, inv


_SBOX, _INV_SBOX = _build_sbox()
_MUL = {c: [_mul(i, c) for i in range(256)] for c in (2, 3, 9, 11, 13, 14)}
_SHIFT = [(i % 4) + 4 * (((i // 4) + (i % 4)) % 4) for i in range(16)]
_INV_SHIFT = [0] * 16
for _i, _v in enumerate(_SHIFT):
    _INV_SHIFT[_v] = _i


class _PyAes:
    def __init__(self, key):
        nk = len(key) // 4
        self._rounds = nk + 6
        w = [list(key[i : i + 4]) for i in range(0, len(key), 4)]
        rcon = 1
        for i in range(nk, 4 * (self._rounds + 1)):
            t = list(w[i - 1])
            if i % nk == 0:
                t = [_SBOX[b] for b in t[1:] + t[:1]]
                t[0] ^= rcon
                rcon = _xtime(rcon)
            elif nk > 6 and i % nk == 4:
                t = [_SBOX[b] for b in t]
            w.append([a ^ b for a, b in zip(w[i - nk], t)])
        self._rk = [sum(w[r * 4 : r * 4 + 4], []) for r in range(self._rounds + 1)]

    def encrypt(self, block):
        s = [a ^ b for a, b in zip(block, self._rk[0])]
        m2, m3 = _MUL[2], _MUL[3]
        for r in range(1, self._rounds + 1):
            s = [_SBOX[s[i]] for i in _SHIFT]
            if r != self._rounds:
                t = []
                for c in range(0, 16, 4):
                    a0, a1, a2, a3 = s[c : c + 4]
                    t += (
                        m2[a0] ^ m3[a1] ^ a2 ^ a3,
                        a0 ^ m2[a1] ^ m3[a2] ^ a3,
                        a0 ^ a1 ^ m2[a2] ^ m3[a3],
                        m3[a0] ^ a1 ^ a2 ^ m2[a3],
                    )
                s = t
            s = [a ^ b for a, b in zip(s, self._rk[r])]
        return bytes(s)

    def decrypt(self, block):
        s = [a ^ b for a, b in zip(block, self._rk[self._rounds])]
        m9, m11, m13, m14 = _MUL[9], _MUL[11], _MUL[13], _MUL[14]
        for r in range(self._rounds - 1, -1, -1):
            s = [_INV_SBOX[s[i]] for i in _INV_SHIFT]
            s = [a ^ b for a, b in zip(s, self._rk[r])]
            if r:
                t = []
                for c in range(0, 16, 4):
                    a0, a1, a2, a3 = s[c : c + 4]
                    t += (
                        m14[a0] ^ m11[a1] ^ m13[a2] ^ m9[a3],
                        m9[a0] ^ m14[a1] ^ m11[a2] ^ m13[a3],
                        m13[a0] ^ m9[a1] ^ m14[a2] ^ m11[a3],
                        m11[a0] ^ m13[a1] ^ m9[a2] ^ m14[a3],
                    )
                s = t
        return bytes(s)


# ---------------------------------------------------------------------------
# MicroPython compatible interface
# ---------------------------------------------------------------------------
try:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
except ImportError:
    Cipher = None


class aes:
    def __init__(self, key, mode, iv=None):
        if len(key) not in (16, 32):
            raise ValueError("key")
        if mode not in (MODE_ECB, MODE_CBC):
            raise ValueError("mode")
        self._key = bytes(key)
        self._mode = mode
        self._iv = bytes(iv) if iv is not None else bytes(16)
        self._dir = None
        self._ctx = None

    def encrypt(self, in_buf, out_buf=None):
        return self._process(True, in_buf, out_buf)

    def decrypt(self, in_buf, out_buf=None):
        return self._process(False, in_buf, out_buf)

    def _process(self, encrypt, in_buf, out_buf):
        if self._dir is None:
            self._dir = encrypt
            self._open(encrypt)
        elif self._dir != encrypt:
            raise OSError("can't encrypt & decrypt")

        data = bytes(in_buf)
        if len(data) % 16:
            raise ValueError("blksize % 16")

        res = self._ctx(data)

        if out_buf is None:
            return res
        out_buf[: len(res)] = res
        return None

    def _open(self, encrypt):
        if Cipher is not None:
            mode = modes.CBC(self._iv) if self._mode == MODE_CBC else modes.ECB()
            c = Cipher(algorithms.AES(self._key), mode)
            ctx = c.encryptor() if encrypt else c.decryptor()
            self._ctx = ctx.update
            return

        py = _PyAes(self._key)
        cbc = self._mode == MODE_CBC

        def run(data):
            out = bytearray()
            for i in range(0, len(data), 16):
                blk = data[i : i + 16]
                if encrypt:
                    if cbc:
                        blk = bytes(a ^ b for a, b in zip(blk, self._iv))
                    o = py.encrypt(blk)
                    if cbc:
                        self._iv = o
                else:
                    o = py.decrypt(blk)
                    if cbc:
                        o, self._iv = bytes(a ^ b for a, b in zip(o, self._iv)), blk
                out += o
            return bytes(out)

        self._ctx = run
