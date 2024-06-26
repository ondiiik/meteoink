from ulogging import getLogger

logger = getLogger(__name__)

BMP = {
    "200d": {1: [94, 94, 0, "bmp"], 2: [46, 47, 4418, "bmp"], 3: [32, 31, 5499, "bmp"]},
    "200n": {
        1: [94, 94, 5995, "bmp"],
        2: [46, 47, 10413, "bmp"],
        3: [32, 31, 11494, "bmp"],
    },
    "300d": {
        1: [94, 80, 11990, "bmp"],
        2: [46, 40, 15750, "bmp"],
        3: [32, 26, 16670, "bmp"],
    },
    "300n": {
        1: [94, 80, 17086, "bmp"],
        2: [46, 40, 20846, "bmp"],
        3: [32, 26, 21766, "bmp"],
    },
    "500d": {
        1: [94, 94, 22182, "bmp"],
        2: [46, 47, 26600, "bmp"],
        3: [32, 31, 27681, "bmp"],
    },
    "500n": {
        1: [94, 94, 28177, "bmp"],
        2: [46, 47, 32595, "bmp"],
        3: [32, 31, 33676, "bmp"],
    },
    "511d": {
        1: [94, 90, 34172, "bmp"],
        2: [48, 45, 38402, "bmp"],
        3: [32, 30, 39482, "bmp"],
    },
    "511n": {
        1: [94, 90, 39962, "bmp"],
        2: [48, 45, 44192, "bmp"],
        3: [32, 30, 45272, "bmp"],
    },
    "520d": {
        1: [94, 94, 45752, "bmp"],
        2: [46, 47, 50170, "bmp"],
        3: [32, 31, 51251, "bmp"],
    },
    "520n": {
        1: [94, 94, 51747, "bmp"],
        2: [46, 47, 56165, "bmp"],
        3: [32, 31, 57246, "bmp"],
    },
    "600d": {
        1: [94, 90, 57742, "bmp"],
        2: [46, 45, 61972, "bmp"],
        3: [32, 30, 63007, "bmp"],
    },
    "600n": {
        1: [94, 90, 63487, "bmp"],
        2: [46, 45, 67717, "bmp"],
        3: [32, 30, 68752, "bmp"],
    },
    "701d": {
        1: [94, 77, 69232, "bmp"],
        2: [48, 38, 72851, "bmp"],
        3: [32, 25, 73763, "bmp"],
    },
    "701n": {
        1: [94, 77, 74163, "bmp"],
        2: [48, 38, 77782, "bmp"],
        3: [32, 25, 78694, "bmp"],
    },
    "800d": {
        1: [94, 94, 79094, "bmp"],
        2: [46, 47, 83512, "bmp"],
        3: [32, 31, 84593, "bmp"],
    },
    "800n": {
        1: [94, 94, 85089, "bmp"],
        2: [46, 47, 89507, "bmp"],
        3: [32, 31, 90588, "bmp"],
    },
    "801d": {
        1: [94, 94, 91084, "bmp"],
        2: [46, 47, 95502, "bmp"],
        3: [32, 31, 96583, "bmp"],
    },
    "801n": {
        1: [94, 94, 97079, "bmp"],
        2: [46, 47, 101497, "bmp"],
        3: [32, 31, 102578, "bmp"],
    },
    "802d": {
        1: [94, 84, 103074, "bmp"],
        2: [46, 42, 107022, "bmp"],
        3: [32, 28, 107988, "bmp"],
    },
    "802n": {
        1: [94, 84, 108436, "bmp"],
        2: [46, 42, 112384, "bmp"],
        3: [32, 28, 113350, "bmp"],
    },
    "803d": {
        1: [94, 50, 113798, "bmp"],
        2: [46, 25, 116148, "bmp"],
        3: [32, 16, 116723, "bmp"],
    },
    "803n": {
        1: [94, 50, 116979, "bmp"],
        2: [46, 25, 119329, "bmp"],
        3: [32, 16, 119904, "bmp"],
    },
    "804d": {
        1: [94, 63, 120160, "bmp"],
        2: [46, 31, 123121, "bmp"],
        3: [32, 21, 123834, "bmp"],
    },
    "804n": {
        1: [94, 63, 124170, "bmp"],
        2: [46, 31, 127131, "bmp"],
        3: [32, 21, 127844, "bmp"],
    },
    "greetings": {1: [960, 540, 128180, "bmp"]},
    "in": {
        1: [38, 32, 387380, "bmp"],
        2: [20, 16, 387988, "bmp"],
        3: [12, 10, 388148, "bmp"],
    },
    "nowifi": {
        1: [32, 27, 388208, "bmp"],
        2: [16, 13, 388640, "bmp"],
        3: [10, 9, 388744, "bmp"],
    },
    "out": {
        1: [44, 32, 388789, "bmp"],
        2: [22, 16, 389493, "bmp"],
        3: [14, 10, 389669, "bmp"],
    },
}
