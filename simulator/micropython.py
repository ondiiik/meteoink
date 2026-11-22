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


# Viper pointer types. In viper code they are compile time annotations (and casts),
# so in PC Python they are just made visible everywhere as no-op casts.
import builtins

for _ptr in ("ptr8", "ptr16", "ptr32"):
    setattr(builtins, _ptr, lambda buf: buf)
