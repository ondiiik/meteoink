from functools import wraps

# Micropython adaptation


def const(val):
    return val


def native(func):
    @wraps(func)
    def wrapper(*args):
        # print('native ->', func, '::', args)
        return func(*args)
    return wrapper


def viper(func):
    @wraps(func)
    def wrapper(*args):
        # print('viper ->', func, '::', args)
        return func(*args)
    return wrapper
