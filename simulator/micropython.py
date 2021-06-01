# Micropython adaptation
def const(val):
    return val


def native(func):
    def wrapper(*args):
        # print('native ->', func, '::', args)
        return func(*args)
    return wrapper


def viper(func):
    def wrapper(*args):
        # print('viper ->', func, '::', args)
        return func(*args)
    return wrapper
