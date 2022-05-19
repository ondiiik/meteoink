from png import Reader
# from struct import unpack
# from uzlib import decompress


def decode(data):
    # '''Very very lighweight PNG reader
    #
    # without defense code, just to read it very quickly
    # '''
    # def read(cnt):
    #     nonlocal data, idx
    #     v = data[idx:idx + cnt]
    #     idx += cnt
    #     return v
    #
    # def drop(cnt):
    #     nonlocal idx
    #     idx += cnt
    #
    # # Operate with memoryview to not to waste by resources
    # data = memoryview(data)
    # idx = 0
    #
    # # Checks PNG header
    # if b'\x89PNG\r\n\x1a\n' != read(8):
    #     raise RuntimeError('Thisi s not PNG!')
    #
    # # Get size of image data
    # backup = idx
    # hdr = read(8)
    # cnt = 0
    #
    # while hdr:
    #     dlen, dtype = unpack('!I4s', hdr)
    #
    #     if dtype == b'IDAT':
    #         cnt += dlen
    #
    #     drop(dlen + 4)
    #     hdr = read(8)
    #
    # # Read image data
    # idx = backup
    # hdr = read(8)
    # compressed = memoryview(bytearray(cnt))
    # i = 0
    #
    # while hdr:
    #     dlen, dtype = unpack('!I4s', hdr)
    #
    #     print(dtype)
    #     if dtype == b'IHDR':
    #         width, height, bits, cltype, compression, fltr, interlace = unpack("!2I5B", read(dlen))
    #         assert width == 256
    #         assert height == 256
    #         assert bits == 8
    #         assert cltype == 6
    #         assert compression == 0
    #         assert fltr == 0
    #         assert interlace == 0
    #     elif dtype == b'IDAT':
    #         compressed[i:i + dlen] = read(dlen)
    #         i += dlen
    #     else:
    #         drop(dlen)
    #
    #     drop(4)
    #     hdr = read(8)
    #
    # # Now we have image data so we have to decompress them
    # raw = memoryview(decompress(compressed))
    # # return 256, 256, [raw[i:i + 1024] for i in range(1, len(raw) + 1, 1025)]

    tile = Reader(data).read()
    return tile[0], tile[1], tuple(tile[2])
