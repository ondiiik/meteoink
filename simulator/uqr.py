import                  re
from framebuf    import FrameBuffer, MONO_HLSB
from micropython import const

ERROR_CORRECT_L = const(1)
ERROR_CORRECT_M = const(0)
ERROR_CORRECT_Q = const(3)
ERROR_CORRECT_H = const(2)

rsPoly_LUT = {
    10: [1, 216, 194, 159, 111, 199, 94, 95, 113, 157, 193],
    13: [1, 137, 73, 227, 17, 177, 17, 52, 13, 46, 43, 83, 132, 120],
    15: [1, 29, 196, 111, 163, 112, 74, 10, 105, 105, 139, 132, 151, 32, 134, 26],
    16: [1, 59, 13, 104, 189, 68, 209, 30, 8, 163, 65, 41, 229, 98, 50, 36, 59],
    17: [1, 119, 66, 83, 120, 119, 22, 197, 83, 249, 41, 143, 134, 85, 53, 125, 99, 79],
    18: [1, 239, 251, 183, 113, 149, 175, 199, 215, 240, 220, 73, 82, 173, 75, 32, 67, 217, 146],
    20: [1, 152, 185, 240, 5, 111, 99, 6, 220, 112, 150, 69, 36, 187, 22, 228, 198, 121, 121, 165, 174],
    22: [1, 89, 179, 131, 176, 182, 244, 19, 189, 69, 40, 28, 137, 29, 123, 67, 253, 86, 218, 230, 26, 145, 245],
    24: [1, 122, 118, 169, 70, 178, 237, 216, 102, 115, 150, 229, 73, 130, 72, 61, 43, 206, 1, 237, 247, 127, 217, 144, 117],
    26: [1, 246, 51, 183, 4, 136, 98, 199, 152, 77, 56, 206, 24, 145, 40, 209, 117, 233, 42, 135, 68, 70, 144, 146, 77, 43, 94]
              }

###
# Base
# 
# Formerly in base.py
###
gexp = b'\x01\x02\x04\x08\x10 @\x80\x1d:t\xe8\xcd\x87\x13&L\x98-Z\xb4u\xea\xc9\x8f\x03\x06\x0c\x180`\xc0\x9d\'N\x9c%J\x945j\xd4\xb5w\xee\xc1\x9f#F\x8c\x05\n\x14(P\xa0]\xbai\xd2\xb9o\xde\xa1_\xbea\xc2\x99/^\xbce\xca\x89\x0f\x1e<x\xf0\xfd\xe7\xd3\xbbk\xd6\xb1\x7f\xfe\xe1\xdf\xa3[\xb6q\xe2\xd9\xafC\x86\x11"D\x88\r\x1a4h\xd0\xbdg\xce\x81\x1f>|\xf8\xed\xc7\x93;v\xec\xc5\x973f\xcc\x85\x17.\\\xb8m\xda\xa9O\x9e!B\x84\x15*T\xa8M\x9a)R\xa4U\xaaI\x929r\xe4\xd5\xb7s\xe6\xd1\xbfc\xc6\x91?~\xfc\xe5\xd7\xb3{\xf6\xf1\xff\xe3\xdb\xabK\x961b\xc4\x957n\xdc\xa5W\xaeA\x82\x192d\xc8\x8d\x07\x0e\x1c8p\xe0\xdd\xa7S\xa6Q\xa2Y\xb2y\xf2\xf9\xef\xc3\x9b+V\xacE\x8a\t\x12$H\x90=z\xf4\xf5\xf7\xf3\xfb\xeb\xcb\x8b\x0b\x16,X\xb0}\xfa\xe9\xcf\x83\x1b6l\xd8\xadG\x8e\x01'
glog = b'\x00\x00\x01\x19\x022\x1a\xc6\x03\xdf3\xee\x1bh\xc7K\x04d\xe0\x0e4\x8d\xef\x81\x1c\xc1i\xf8\xc8\x08Lq\x05\x8ae/\xe1$\x0f!5\x93\x8e\xda\xf0\x12\x82E\x1d\xb5\xc2}j\'\xf9\xb9\xc9\x9a\txM\xe4r\xa6\x06\xbf\x8bbf\xdd0\xfd\xe2\x98%\xb3\x10\x91"\x886\xd0\x94\xce\x8f\x96\xdb\xbd\xf1\xd2\x13\\\x838F@\x1eB\xb6\xa3\xc3H~nk:(T\xfa\x85\xba=\xca^\x9b\x9f\n\x15y+N\xd4\xe5\xacs\xf3\xa7W\x07p\xc0\xf7\x8c\x80c\rgJ\xde\xed1\xc5\xfe\x18\xe3\xa5\x99w&\xb8\xb4|\x11D\x92\xd9# \x89.7?\xd1[\x95\xbc\xcf\xcd\x90\x87\x97\xb2\xdc\xfc\xbea\xf2V\xd3\xab\x14*]\x9e\x84<9SGmA\xa2\x1f-C\xd8\xb7{\xa4v\xc4\x17I\xec\x7f\x0co\xf6l\xa1;R)\x9dU\xaa\xfb`\x86\xb1\xbb\xcc>Z\xcbY_\xb0\x9c\xa9\xa0Q\x0b\xf5\x16\xebzu,\xd7O\xae\xd5\xe9\xe6\xe7\xad\xe8t\xd6\xf4\xea\xa8PX\xaf'

RS_BLOCK_OFFSET = {
    ERROR_CORRECT_L: 0,
    ERROR_CORRECT_M: 1,
    ERROR_CORRECT_Q: 2,
    ERROR_CORRECT_H: 3,
}

RS_BLOCK_TABLE = (b'\x01\x1a\x13',
                  b'\x01\x1a\x10',
                  b'\x01\x1a\r',
                  b'\x01\x1a\t',
                  b'\x01,"',
                  b'\x01,\x1c',
                  b'\x01,\x16',
                  b'\x01,\x10',
                  b'\x01F7',
                  b'\x01F,',
                  b'\x02#\x11',
                  b'\x02#\r',
                  b'\x01dP',
                  b'\x022 ',
                  b'\x022\x18',
                  b'\x04\x19\t',
                  b'\x01\x86l',
                  b'\x02C+',
                  b'\x02!\x0f\x02"\x10',
                  b'\x02!\x0b\x02"\x0c',
                  b'\x02VD',
                  b'\x04+\x1b',
                  b'\x04+\x13',
                  b'\x04+\x0f',
                  b'\x02bN',
                  b'\x041\x1f',
                  b'\x02 \x0e\x04!\x0f',
                  b"\x04\'\r\x01(\x0e",
                  b'\x02ya',
                  b"\x02<&\x02=\'",
                  b'\x04(\x12\x02,\x13',
                  b'\x04(\x0e\x02,\x0f',
                  b'\x02\x92t',
                  b'\x03:$\x02;%',
                  b'\x04$\x10\x04%\x11',
                  b'\x04$\x0c\x04%\r',
                  b'\x02VD\x02WE',
                  b'\x04E+\x01F,',
                  b'\x06+\x13\x02,\x14',
                  b'\x06+\x0f\x02,\x10',
                  b'\x04eQ',
                  b'\x01P2\x04Q3',
                  b'\x042\x16\x043\x17',
                  b'\x03$\x0c\x08%\r',
                  b'\x02t\\\x02u]',
                  b'\x06:$\x02;%',
                  b'\x04.\x14\x06/\x15',
                  b'\x07*\x0e\x04+\x0f',
                  b'\x04\x85k',
                  b'\x08;%\x01<&',
                  b'\x08,\x14\x04-\x15',
                  b'\x0c!\x0b\x04"\x0c',
                  b'\x03\x91s\x01\x92t',
                  b'\x04@(\x05A,',
                  b'\x0b$\x10\x05%\x11',
                  b'\x0b$\x0c\x05%\r',
                  b'\x05mW\x01nX',
                  b'\x05A,\x05B*',
                  b'\x056\x18\x077\x19',
                  b'\x0b$\x0c\x07%\r',
                  b'\x05zb\x01{c',
                  b'\x07I-\x03J.',
                  b'\x0f+\x13\x02,\x14',
                  b'\x03-\x0f\r.\x10',
                  b'\x01\x87k\x05\x88l',
                  b'\nJ.\x01K/',
                  b'\x012\x16\x0f3\x17',
                  b'\x02*\x0e\x11+\x0f',
                  b'\x05\x96x\x01\x97y',
                  b'\tE+\x04F,',
                  b'\x112\x16\x013\x17',
                  b'\x02*\x0e\x13+\x0f',
                  b'\x03\x8dq\x04\x8er',
                  b'\x03F,\x0bG-',
                  b'\x11/\x15\x040\x16',
                  b"\t\'\r\x10(\x0e",
                  b'\x03\x87k\x05\x88l',
                  b'\x03C,\rD*',
                  b'\x0f6\x18\x057\x19',
                  b'\x0f+\x0f\n,\x10',
                  b'\x04\x90t\x04\x91u',
                  b'\x11D*',
                  b'\x112\x16\x063\x17',
                  b'\x13.\x10\x06/\x11',
                  b'\x02\x8bo\x07\x8cp',
                  b'\x11J.',
                  b'\x076\x18\x107\x19',
                  b'"%\r',
                  b'\x04\x97y\x05\x98z',
                  b'\x04K/\x0eL0',
                  b'\x0b6\x18\x0e7\x19',
                  b'\x10-\x0f\x0e.\x10',
                  b'\x06\x93u\x04\x94v',
                  b'\x06I-\x0eJ.',
                  b'\x0b6\x18\x107\x19',
                  b'\x1e.\x10\x02/\x11',
                  b'\x08\x84j\x04\x85k',
                  b'\x08K/\rL0',
                  b'\x076\x18\x167\x19',
                  b'\x16-\x0f\r.\x10',
                  b'\n\x8er\x02\x8fs',
                  b'\x13J.\x04K/',
                  b'\x1c2\x16\x063\x17',
                  b'!.\x10\x04/\x11',
                  b'\x08\x98z\x04\x99{',
                  b'\x16I-\x03J.',
                  b'\x085\x17\x1a6\x18',
                  b'\x0c-\x0f\x1c.\x10',
                  b'\x03\x93u\n\x94v',
                  b'\x03I-\x17J.',
                  b'\x046\x18\x1f7\x19',
                  b'\x0b-\x0f\x1f.\x10',
                  b'\x07\x92t\x07\x93u',
                  b'\x15I-\x07J.',
                  b'\x015\x17%6\x18',
                  b'\x13-\x0f\x1a.\x10',
                  b'\x05\x91s\n\x92t',
                  b'\x13K/\nL0',
                  b'\x0f6\x18\x197\x19',
                  b'\x17-\x0f\x19.\x10',
                  b'\r\x91s\x03\x92t',
                  b'\x02J.\x1dK/',
                  b'*6\x18\x017\x19',
                  b'\x17-\x0f\x1c.\x10',
                  b'\x11\x91s',
                  b'\nJ.\x17K/',
                  b'\n6\x18#7\x19',
                  b'\x13-\x0f#.\x10',
                  b'\x11\x91s\x01\x92t',
                  b'\x0eJ.\x15K/',
                  b'\x1d6\x18\x137\x19',
                  b'\x0b-\x0f..\x10',
                  b'\r\x91s\x06\x92t',
                  b'\x0eJ.\x17K/',
                  b',6\x18\x077\x19',
                  b';.\x10\x01/\x11',
                  b'\x0c\x97y\x07\x98z',
                  b'\x0cK/\x1aL0',
                  b"\'6\x18\x0e7\x19",
                  b'\x16-\x0f,.\x10',
                  b'\x06\x97y\x0e\x98z',
                  b'\x06K/"L0',
                  b'.6\x18\n7\x19',
                  b'\x02-\x0f@.\x10',
                  b'\x11\x98z\x04\x99{',
                  b'\x1dJ.\x0eK/',
                  b'16\x18\n7\x19',
                  b'\x18-\x0f..\x10',
                  b'\x04\x98z\x12\x99{',
                  b'\rJ. K/',
                  b'06\x18\x0e7\x19',
                  b'*-\x0f .\x10',
                  b'\x14\x93u\x04\x94v',
                  b'(K/\x07L0',
                  b'+6\x18\x167\x19',
                  b'\n-\x0fC.\x10',
                  b'\x13\x94v\x06\x95w',
                  b'\x12K/\x1fL0',
                  b'"6\x18"7\x19',
                  b'\x14-\x0f=.\x10')


class Polynomial:

    def __init__(self, num, shift):
        if not num:  # pragma: no cover
            raise Exception("%s/%s" % (len(num), shift))

        for offset in range(len(num)):
            if num[offset] != 0:
                break
        else:
            offset += 1

        self.num = num[offset:] + [0] * shift

    def __getitem__(self, index):
        return self.num[index]

    def __iter__(self):
        return iter(self.num)

    def __len__(self):
        return len(self.num)

    def __mul__(self, other):
        num = [0] * (len(self) + len(other) - 1)

        for i, item in enumerate(self):
            for j, other_item in enumerate(other):
                num[i + j] ^= gexp[(glog[item] + glog[other_item]) % 255]

        return Polynomial(num, 0)

    ###
    # EDIT
    ###

    def __mod__(self, other):

        this = self

        while True:
            difference = len(this) - len(other)

            if difference < 0:
                break

            ratio = glog[this[0]] - glog[other[0]]

            num = [
                item ^ gexp[(glog[other_item] + ratio) % 255]
                for item, other_item in zip(this, other)]
            if difference:
                num.extend(this[-difference:])

            this = Polynomial(num, 0)

        return this


class RSBlock:

    def __init__(self, total_count, data_count):
        self.total_count = total_count
        self.data_count = data_count


def make_rs_blocks(version, error_correction):
    if error_correction not in RS_BLOCK_OFFSET:  # pragma: no cover
        raise Exception(
            "bad rs block @ version: %s / error_correction: %s" %
            (version, error_correction))
    offset = RS_BLOCK_OFFSET[error_correction]
    rs_block = RS_BLOCK_TABLE[(version - 1) * 4 + offset]

    blocks = []

    for i in range(0, len(rs_block), 3):
        count, total_count, data_count = rs_block[i:i + 3]
        for j in range(count):
            blocks.append(RSBlock(total_count, data_count))

    return blocks


###
# Utilities
# 
# Formerly in utils.py
###

# QR encoding modes.
MODE_NUMBER = 1 << 0
MODE_ALPHA_NUM = 1 << 1
MODE_8BIT_BYTE = 1 << 2
MODE_KANJI = 1 << 3

# Encoding mode sizes.
MODE_SIZE_SMALL = {
    MODE_NUMBER: 10,
    MODE_ALPHA_NUM: 9,
    MODE_8BIT_BYTE: 8,
    MODE_KANJI: 8,
}
MODE_SIZE_MEDIUM = {
    MODE_NUMBER: 12,
    MODE_ALPHA_NUM: 11,
    MODE_8BIT_BYTE: 16,
    MODE_KANJI: 10,
}
MODE_SIZE_LARGE = {
    MODE_NUMBER: 14,
    MODE_ALPHA_NUM: 13,
    MODE_8BIT_BYTE: 16,
    MODE_KANJI: 12,
}

ALPHA_NUM = b'0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:'
ESCAPED_ALPHA_NUM = b'0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ\\ \\$\\%\\*\\+\\-\\.\\/\\:'

RE_ALPHA_NUM = re.compile(b'^[' + ESCAPED_ALPHA_NUM + b']*\Z')

# The number of bits for numeric delimited data lengths.
NUMBER_LENGTH = {3: 10, 2: 7, 1: 4}

PATTERN_POSITION_TABLE = [
    [],
    [6, 18],
    [6, 22],
    [6, 26],
    [6, 30],
    [6, 34],
    [6, 22, 38],
    [6, 24, 42],
    [6, 26, 46],
    [6, 28, 50],
    [6, 30, 54],
    [6, 32, 58],
    [6, 34, 62],
    [6, 26, 46, 66],
    [6, 26, 48, 70],
    [6, 26, 50, 74],
    [6, 30, 54, 78],
    [6, 30, 56, 82],
    [6, 30, 58, 86],
    [6, 34, 62, 90],
    [6, 28, 50, 72, 94],
    [6, 26, 50, 74, 98],
    [6, 30, 54, 78, 102],
    [6, 28, 54, 80, 106],
    [6, 32, 58, 84, 110],
    [6, 30, 58, 86, 114],
    [6, 34, 62, 90, 118],
    [6, 26, 50, 74, 98, 122],
    [6, 30, 54, 78, 102, 126],
    [6, 26, 52, 78, 104, 130],
    [6, 30, 56, 82, 108, 134],
    [6, 34, 60, 86, 112, 138],
    [6, 30, 58, 86, 114, 142],
    [6, 34, 62, 90, 118, 146],
    [6, 30, 54, 78, 102, 126, 150],
    [6, 24, 50, 76, 102, 128, 154],
    [6, 28, 54, 80, 106, 132, 158],
    [6, 32, 58, 84, 110, 136, 162],
    [6, 26, 54, 82, 110, 138, 166],
    [6, 30, 58, 86, 114, 142, 170]
]

G15 = (
    (1 << 10) | (1 << 8) | (1 << 5) | (1 << 4) | (1 << 2) | (1 << 1) |
    (1 << 0))
G18 = (
    (1 << 12) | (1 << 11) | (1 << 10) | (1 << 9) | (1 << 8) | (1 << 5) |
    (1 << 2) | (1 << 0))
G15_MASK = (1 << 14) | (1 << 12) | (1 << 10) | (1 << 4) | (1 << 1)

PAD0 = 0xEC
PAD1 = 0x11

# Precompute bit count limits, indexed by error correction level and code size
_data_count = lambda block: block.data_count
BIT_LIMIT_TABLE = [
    [0] + [8*sum(map(_data_count, make_rs_blocks(version, error_correction)))
           for version in range(1, 41)]
    for error_correction in range(4)
]


def BCH_type_info(data):
        d = data << 10
        while BCH_digit(d) - BCH_digit(G15) >= 0:
            d ^= (G15 << (BCH_digit(d) - BCH_digit(G15)))

        return ((data << 10) | d) ^ G15_MASK


def BCH_type_number(data):
    d = data << 12
    while BCH_digit(d) - BCH_digit(G18) >= 0:
        d ^= (G18 << (BCH_digit(d) - BCH_digit(G18)))
    return (data << 12) | d


def BCH_digit(data):
    digit = 0
    while data != 0:
        digit += 1
        data >>= 1
    return digit


def pattern_position(version):
    return PATTERN_POSITION_TABLE[version - 1]


def make_mask_func(pattern):
    ###
    # Return the mask function for the given mask pattern.
    ###
    if pattern == 0:   # 000
        return lambda i, j: (i + j) % 2 == 0
    if pattern == 1:   # 001
        return lambda i, j: i % 2 == 0
    if pattern == 2:   # 010
        return lambda i, j: j % 3 == 0
    if pattern == 3:   # 011
        return lambda i, j: (i + j) % 3 == 0
    if pattern == 4:   # 100
        return lambda i, j: (int(i / 2) + int(j / 3)) % 2 == 0
    if pattern == 5:  # 101
        return lambda i, j: (i * j) % 2 + (i * j) % 3 == 0
    if pattern == 6:  # 110
        return lambda i, j: ((i * j) % 2 + (i * j) % 3) % 2 == 0
    if pattern == 7:  # 111
        return lambda i, j: ((i * j) % 3 + (i + j) % 2) % 2 == 0
    raise TypeError("Bad mask pattern: " + pattern)  # pragma: no cover


def mode_sizes_for_version(version):
    if version < 10:
        return MODE_SIZE_SMALL
    elif version < 27:
        return MODE_SIZE_MEDIUM
    else:
        return MODE_SIZE_LARGE


def length_in_bits(mode, version):
    if mode not in (
            MODE_NUMBER, MODE_ALPHA_NUM, MODE_8BIT_BYTE, MODE_KANJI):
        raise TypeError("Invalid mode (%s)" % mode)  # pragma: no cover

    if version < 1 or version > 40:  # pragma: no cover
        raise ValueError(
            "Invalid version (was %s, expected 1 to 40)" % version)

    return mode_sizes_for_version(version)[mode]


def make_lost_point(modules):
    modules_count = len(modules)

    lost_point = 0

    lost_point = _lost_point_level1(modules, modules_count)
    lost_point += _lost_point_level2(modules, modules_count)
    lost_point += _lost_point_level3(modules, modules_count)
    lost_point += _lost_point_level4(modules, modules_count)

    return lost_point


def _lost_point_level1(modules, modules_count):
    lost_point = 0

    modules_range = range(modules_count)
    container = [0] * (modules_count + 1)

    for row in modules_range:
        this_row = modules[row]
        previous_color = this_row[0]
        length = 0
        for col in modules_range:
            if this_row[col] == previous_color:
                length += 1
            else:
                if length >= 5:
                    container[length] += 1
                length = 1
                previous_color = this_row[col]
        if length >= 5:
            container[length] += 1

    for col in modules_range:
        previous_color = modules[0][col]
        length = 0
        for row in modules_range:
            if modules[row][col] == previous_color:
                length += 1
            else:
                if length >= 5:
                    container[length] += 1
                length = 1
                previous_color = modules[row][col]
        if length >= 5:
            container[length] += 1

    lost_point += sum(container[each_length] * (each_length - 2)
        for each_length in range(5, modules_count + 1))

    return lost_point


def _lost_point_level2(modules, modules_count):
    lost_point = 0

    modules_range = range(modules_count - 1)
    for row in modules_range:
        this_row = modules[row]
        next_row = modules[row + 1]
        # use iter() and next() to skip next four-block. e.g.
        # d a f   if top-right a != b botton-right,
        # c b e   then both abcd and abef won't lost any point.
        modules_range_iter = iter(modules_range)
        for col in modules_range_iter:
            top_right = this_row[col + 1]
            if top_right != next_row[col + 1]:
                # reduce 33.3% of runtime via next().
                # None: raise nothing if there is no next item.
                try:
                    next(modules_range_iter)
                except StopIteration:
                    pass
            elif top_right != this_row[col]:
                continue
            elif top_right != next_row[col]:
                continue
            else:
                lost_point += 3

    return lost_point


def _lost_point_level3(modules, modules_count):
    # 1 : 1 : 3 : 1 : 1 ratio (dark:light:dark:light:dark) pattern in
    # row/column, preceded or followed by light area 4 modules wide. From ISOIEC.
    # pattern1:     10111010000
    # pattern2: 00001011101
    modules_range = range(modules_count)
    modules_range_short = range(modules_count-10)
    lost_point = 0

    for row in modules_range:
        this_row = modules[row]
        modules_range_short_iter = iter(modules_range_short)
        col = 0
        for col in modules_range_short_iter:
            if (
                        not this_row[col + 1]
                    and this_row[col + 4]
                    and not this_row[col + 5]
                    and this_row[col + 6]
                    and not this_row[col + 9]
                and (
                        this_row[col + 0]
                    and this_row[col + 2]
                    and this_row[col + 3]
                    and not this_row[col + 7]
                    and not this_row[col + 8]
                    and not this_row[col + 10]
                or
                        not this_row[col + 0]
                    and not this_row[col + 2]
                    and not this_row[col + 3]
                    and this_row[col + 7]
                    and this_row[col + 8]
                    and this_row[col + 10]
                    )
                ):
                lost_point += 40
# horspool algorithm.
# if this_row[col + 10] == True,  pattern1 shift 4, pattern2 shift 2. So min=2.
# if this_row[col + 10] == False, pattern1 shift 1, pattern2 shift 1. So min=1.
            if this_row[col + 10]:
                try:
                    next(modules_range_short_iter)
                except StopIteration:
                    pass

    for col in modules_range:
        modules_range_short_iter = iter(modules_range_short)
        row = 0
        for row in modules_range_short_iter:
            if (
                        not modules[row + 1][col]
                    and modules[row + 4][col]
                    and not modules[row + 5][col]
                    and modules[row + 6][col]
                    and not modules[row + 9][col]
                and (
                        modules[row + 0][col]
                    and modules[row + 2][col]
                    and modules[row + 3][col]
                    and not modules[row + 7][col]
                    and not modules[row + 8][col]
                    and not modules[row + 10][col]
                or
                        not modules[row + 0][col]
                    and not modules[row + 2][col]
                    and not modules[row + 3][col]
                    and modules[row + 7][col]
                    and modules[row + 8][col]
                    and modules[row + 10][col]
                    )
                ):
                lost_point += 40
            if modules[row + 10][col]:
                try:
                    next(modules_range_short_iter)
                except StopIteration:
                    pass

    return lost_point


def _lost_point_level4(modules, modules_count):
    dark_count = sum(map(sum, modules))
    percent = float(dark_count) / (modules_count**2)
    # Every 5% departure from 50%, rating++
    rating = int(abs(percent * 100 - 50) / 5)
    return rating * 10


def optimal_data_chunks(data, minimum=4):
    ###
    # An iterator returning QRData chunks optimized to the data content.
    #
    # :param minimum: The minimum number of bytes in a row to split as a chunk.
    ###
    data = to_bytestring(data)
    re_repeat = (
        b'{' + str(minimum).encode('ascii') + b',}')
    num_pattern = re.compile(b'\d' + re_repeat)
    num_bits = _optimal_split(data, num_pattern)
    alpha_pattern = re.compile(
        b'[' + ESCAPED_ALPHA_NUM + b']' + re_repeat)
    for is_num, chunk in num_bits:
        if is_num:
            yield QRData(chunk, mode=MODE_NUMBER, check_data=False)
        else:
            for is_alpha, sub_chunk in _optimal_split(chunk, alpha_pattern):
                if is_alpha:
                    mode = MODE_ALPHA_NUM
                else:
                    mode = MODE_8BIT_BYTE
                yield QRData(sub_chunk, mode=mode, check_data=False)


def _optimal_split(data, pattern):
    while data:
        match = pattern.search(data)
        if not match:
            break
        start, end = match.start(), match.end()
        if start:
            yield False, data[:start]
        yield True, data[start:end]
        data = data[end:]
    if data:
        yield False, data


def to_bytestring(data):
    ###
    # Convert data to a (utf-8 encoded) byte-string if it isn't a byte-string
    # already.
    ###
    if not isinstance(data, bytes):
        data = str(data).encode('utf-8')
    return data


def optimal_mode(data):
    ###
    # Calculate the optimal mode for this chunk of data.
    ###
    if data.isdigit():
        return MODE_NUMBER
    if RE_ALPHA_NUM.match(data):
        return MODE_ALPHA_NUM
    return MODE_8BIT_BYTE


class QRData:
    def __init__(self, data, mode=None, check_data=True):
        if check_data:
            data = to_bytestring(data)

        if mode is None:
            self.mode = optimal_mode(data)
        else:
            self.mode = mode
            if mode not in (MODE_NUMBER, MODE_ALPHA_NUM, MODE_8BIT_BYTE):
                raise TypeError("Invalid mode (%s)" % mode)  # pragma: no cover
            if check_data and mode < optimal_mode(data):  # pragma: no cover
                raise ValueError(
                    "Provided data can not be represented in mode "
                    "{0}".format(mode))

        self.data = data

    def __len__(self):
        return len(self.data)

    def write(self, buffer):
        if self.mode == MODE_NUMBER:
            for i in range(0, len(self.data), 3):
                chars = self.data[i:i + 3]
                bit_length = NUMBER_LENGTH[len(chars)]
                buffer.put(int(chars), bit_length)
        elif self.mode == MODE_ALPHA_NUM:
            for i in range(0, len(self.data), 2):
                chars = self.data[i:i + 2]
                if len(chars) > 1:
                    buffer.put(
                        ALPHA_NUM.find(chars[0]) * 45 +
                        ALPHA_NUM.find(chars[1]), 11)
                else:
                    buffer.put(ALPHA_NUM.find(chars), 6)
        else:
            data = self.data
            for c in data:
                buffer.put(c, 8)

    def __repr__(self):
        return repr(self.data)


class BitBuffer:

    def __init__(self):
        self.buffer = []
        self.length = 0

    def __repr__(self):
        return ".".join([str(n) for n in self.buffer])

    def get(self, index):
        buf_index = int(index / 8)
        return ((self.buffer[buf_index] >> (7 - index % 8)) & 1) == 1

    def put(self, num, length):
        for i in range(length):
            self.put_bit(((num >> (length - i - 1)) & 1) == 1)

    def __len__(self):
        return self.length

    def put_bit(self, bit):
        buf_index = self.length // 8
        if len(self.buffer) <= buf_index:
            self.buffer.append(0)
        if bit:
            self.buffer[buf_index] |= (0x80 >> (self.length % 8))
        self.length += 1


def create_bytes(buffer, rs_blocks):
    offset = 0

    maxDcCount = 0
    maxEcCount = 0

    dcdata = [0] * len(rs_blocks)
    ecdata = [0] * len(rs_blocks)

    for r in range(len(rs_blocks)):

        dcCount = rs_blocks[r].data_count
        ecCount = rs_blocks[r].total_count - dcCount

        maxDcCount = max(maxDcCount, dcCount)
        maxEcCount = max(maxEcCount, ecCount)

        dcdata[r] = [0] * dcCount

        for i in range(len(dcdata[r])):
            dcdata[r][i] = 0xff & buffer.buffer[i + offset]
        offset += dcCount

        # Get error correction polynomial.
        if ecCount in rsPoly_LUT:
            rsPoly = Polynomial(rsPoly_LUT[ecCount], 0)
        else:
            rsPoly = Polynomial([1], 0)
            for i in range(ecCount):
                rsPoly = rsPoly * Polynomial([1, gexp[i % 255]], 0)

        rawPoly = Polynomial(dcdata[r], len(rsPoly) - 1)

        modPoly = rawPoly % rsPoly
        ecdata[r] = [0] * (len(rsPoly) - 1)
        for i in range(len(ecdata[r])):
            modIndex = i + len(modPoly) - len(ecdata[r])
            if (modIndex >= 0):
                ecdata[r][i] = modPoly[modIndex]
            else:
                ecdata[r][i] = 0

    totalCodeCount = 0
    for rs_block in rs_blocks:
        totalCodeCount += rs_block.total_count

    data = [None] * totalCodeCount
    index = 0

    for i in range(maxDcCount):
        for r in range(len(rs_blocks)):
            if i < len(dcdata[r]):
                data[index] = dcdata[r][i]
                index += 1

    for i in range(maxEcCount):
        for r in range(len(rs_blocks)):
            if i < len(ecdata[r]):
                data[index] = ecdata[r][i]
                index += 1

    return data


def create_data(version, error_correction, data_list):

    buffer = BitBuffer()
    for data in data_list:
        buffer.put(data.mode, 4)
        buffer.put(len(data), length_in_bits(data.mode, version))
        data.write(buffer)

    # Calculate the maximum number of bits for the given version.
    rs_blocks = make_rs_blocks(version, error_correction)
    bit_limit = 0
    for block in rs_blocks:
        bit_limit += block.data_count * 8

    if len(buffer) > bit_limit:
        raise RuntimeError(
            "Code length overflow. Data size (%s) > size available (%s)" %
            (len(buffer), bit_limit))

    # Terminate the bits (add up to four 0s).
    for i in range(min(bit_limit - len(buffer), 4)):
        buffer.put_bit(False)

    # Delimit the string into 8-bit words, padding with 0s if necessary.
    delimit = len(buffer) % 8
    if delimit:
        for i in range(8 - delimit):
            buffer.put_bit(False)

    # Add special alternating padding bitstrings until buffer is full.
    bytes_to_fill = (bit_limit - len(buffer)) // 8
    for i in range(bytes_to_fill):
        if i % 2 == 0:
            buffer.put(PAD0, 8)
        else:
            buffer.put(PAD1, 8)

    return create_bytes(buffer, rs_blocks)


###
# Main
# 
# Formerly in app.py
###
def make(data=None, **kwargs):
    qr = QRCode(**kwargs)
    qr.add_data(data)
    return qr.make_image()


def _check_version(version):
    if version < 1 or version > 40:
        raise ValueError(
            "Invalid version (was %s, expected 1 to 40)" % version)


def _check_box_size(size):
    if int(size) <= 0:
        raise ValueError(
            "Invalid box size (was %s, expected larger than 0)" % size)


def _check_mask_pattern(mask_pattern):
    if mask_pattern is None:
        return
    if not isinstance(mask_pattern, int):
        raise TypeError(
            "Invalid mask pattern (was %s, expected int)" % type(mask_pattern))
    if mask_pattern < 0 or mask_pattern > 7:
        raise ValueError(
            "Mask pattern should be in range(8) (got %s)" % mask_pattern)

class QRCode:

    def __init__(self, version=None,
                 error_correction=ERROR_CORRECT_M,
                 box_size=10, border=4,
                 mask_pattern=None):
        _check_box_size(box_size)
        self.version = version and int(version)
        self.error_correction = int(error_correction)
        self.box_size = int(box_size)
        # Spec says border should be at least four boxes wide, but allow for
        # any (e.g. for producing printable QR codes).
        self.border = int(border)
        _check_mask_pattern(mask_pattern)
        self.mask_pattern = mask_pattern

        self.clear()

    def clear(self):
        ###
        # Reset the internal data.
        ###
        self.modules = None
        self.modules_count = 0
        self.data_cache = None
        self.data_list = []

    def add_data(self, data):
        if isinstance(data, QRData):
            self.data_list.append(data)
        else:
            self.data_list.append(QRData(data))
        self.data_cache = None

    def make(self, fit=True):
        ###
        # Compile the data into a QR Code array.
        #
        # :param fit: If ``True`` (or if a size has not been provided), find the
        #     best fit for the data to avoid data overflow errors.
        ###
        if fit or (self.version is None):
            self.best_fit(start=self.version)
        if self.mask_pattern is None:
            self.makeImpl(False, self.best_mask_pattern())
        else:
            self.makeImpl(False, self.mask_pattern)

    def makeImpl(self, test, mask_pattern):
        _check_version(self.version)
        self.modules_count = self.version * 4 + 17
        self.modules = [None] * self.modules_count

        for row in range(self.modules_count):

            self.modules[row] = [None] * self.modules_count

            for col in range(self.modules_count):
                self.modules[row][col] = None   # (col + row) % 3

        self.setup_position_probe_pattern(0, 0)
        self.setup_position_probe_pattern(self.modules_count - 7, 0)
        self.setup_position_probe_pattern(0, self.modules_count - 7)
        self.setup_position_adjust_pattern()
        self.setup_timing_pattern()
        self.setup_type_info(test, mask_pattern)

        if self.version >= 7:
            self.setup_type_number(test)

        if self.data_cache is None:
            self.data_cache = create_data(
                self.version, self.error_correction, self.data_list)
        self.map_data(self.data_cache, mask_pattern)

    def setup_position_probe_pattern(self, row, col):
        for r in range(-1, 8):

            if row + r <= -1 or self.modules_count <= row + r:
                continue

            for c in range(-1, 8):

                if col + c <= -1 or self.modules_count <= col + c:
                    continue

                if (0 <= r and r <= 6 and (c == 0 or c == 6)
                        or (0 <= c and c <= 6 and (r == 0 or r == 6))
                        or (2 <= r and r <= 4 and 2 <= c and c <= 4)):
                    self.modules[row + r][col + c] = True
                else:
                    self.modules[row + r][col + c] = False

    def best_fit(self, start=None):
        ###
        # Find the minimum size required to fit in the data.
        ###
        if start is None:
            start = 1
        _check_version(start)

        # Corresponds to the code in create_data, except we don't yet know
        # version, so optimistically assume start and check later
        mode_sizes = mode_sizes_for_version(start)
        buffer = BitBuffer()
        for data in self.data_list:
            buffer.put(data.mode, 4)
            buffer.put(len(data), mode_sizes[data.mode])
            data.write(buffer)

        needed_bits = len(buffer)

        self.version = start
        end = len(BIT_LIMIT_TABLE[self.error_correction])

        while (self.version < end and 
               needed_bits > BIT_LIMIT_TABLE[self.error_correction][self.version]):
            self.version += 1

        if self.version == 41:
            raise RuntimeError('Version overflow')

        # Now check whether we need more bits for the mode sizes, recursing if
        # our guess was too low
        if mode_sizes is not mode_sizes_for_version(self.version):
            self.best_fit(start=self.version)
        return self.version

    def best_mask_pattern(self):
        ###
        # Find the most efficient mask pattern.
        ###
        min_lost_point = 0
        pattern = 0

        for i in range(8):
            self.makeImpl(True, i)

            lost_point = make_lost_point(self.modules)

            if i == 0 or min_lost_point > lost_point:
                min_lost_point = lost_point
                pattern = i

        return pattern


    def setup_timing_pattern(self):
        for r in range(8, self.modules_count - 8):
            if self.modules[r][6] is not None:
                continue
            self.modules[r][6] = (r % 2 == 0)

        for c in range(8, self.modules_count - 8):
            if self.modules[6][c] is not None:
                continue
            self.modules[6][c] = (c % 2 == 0)

    def setup_position_adjust_pattern(self):
        pos = pattern_position(self.version)

        for i in range(len(pos)):

            for j in range(len(pos)):

                row = pos[i]
                col = pos[j]

                if self.modules[row][col] is not None:
                    continue

                for r in range(-2, 3):

                    for c in range(-2, 3):

                        if (r == -2 or r == 2 or c == -2 or c == 2 or
                                (r == 0 and c == 0)):
                            self.modules[row + r][col + c] = True
                        else:
                            self.modules[row + r][col + c] = False

    def setup_type_number(self, test):
        bits = BCH_type_number(self.version)

        for i in range(18):
            mod = (not test and ((bits >> i) & 1) == 1)
            self.modules[i // 3][i % 3 + self.modules_count - 8 - 3] = mod

        for i in range(18):
            mod = (not test and ((bits >> i) & 1) == 1)
            self.modules[i % 3 + self.modules_count - 8 - 3][i // 3] = mod

    def setup_type_info(self, test, mask_pattern):
        data = (self.error_correction << 3) | mask_pattern
        bits = BCH_type_info(data)

        # vertical
        for i in range(15):

            mod = (not test and ((bits >> i) & 1) == 1)

            if i < 6:
                self.modules[i][8] = mod
            elif i < 8:
                self.modules[i + 1][8] = mod
            else:
                self.modules[self.modules_count - 15 + i][8] = mod

        # horizontal
        for i in range(15):

            mod = (not test and ((bits >> i) & 1) == 1)

            if i < 8:
                self.modules[8][self.modules_count - i - 1] = mod
            elif i < 9:
                self.modules[8][15 - i - 1 + 1] = mod
            else:
                self.modules[8][15 - i - 1] = mod

        # fixed module
        self.modules[self.modules_count - 8][8] = (not test)

    def map_data(self, data, mask_pattern):
        inc = -1
        row = self.modules_count - 1
        bitIndex = 7
        byteIndex = 0

        mask_func = make_mask_func(mask_pattern)

        data_len = len(data)

        for col in range(self.modules_count - 1, 0, -2):

            if col <= 6:
                col -= 1

            col_range = (col, col-1)

            while True:

                for c in col_range:

                    if self.modules[row][c] is None:

                        dark = False

                        if byteIndex < data_len:
                            dark = (((data[byteIndex] >> bitIndex) & 1) == 1)

                        if mask_func(row, c):
                            dark = not dark

                        self.modules[row][c] = dark
                        bitIndex -= 1

                        if bitIndex == -1:
                            byteIndex += 1
                            bitIndex = 7

                row += inc

                if row < 0 or self.modules_count <= row:
                    row -= inc
                    inc = -inc
                    break

    def get_matrix(self):
        if self.data_cache is None:
            self.make()
        
        if not self.border:
            return self.modules
        
        width = len(self.modules) + self.border * 2
        buf   = bytearray(width * (width + 7) // 8)
        fb    = FrameBuffer(buf, width, width, MONO_HLSB)
        fb.fill(0)
        
        y = self.border
        for module in self.modules:
            x = self.border
            for p in module:
                fb.pixel(x, y, p)
                x += 1
            y += 1
        
        return (fb, width)
