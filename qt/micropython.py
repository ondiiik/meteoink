# Micropython adaptation
def const(val):
    return val


def native(func):
    def wrapper(*args):
        func(*args)
    return wrapper


def viper(func):
    def wrapper(*args):
        func(*args)
    return wrapper
