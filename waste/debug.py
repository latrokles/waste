import functools
import os


def debugmethod(func):
    is_debug = os.getenv("DEBUG")

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        message = ""
        output = None
        if is_debug:
            message = f"func={func.__name__} called with {args=}, {kwargs=}"

        try:
            output = func(self, *args, **kwargs)
            return output
        finally:
            if is_debug:
                print(f"{message}, returned {output=}")

    return wrapper


def debugfunc(func):
    is_debug = os.getenv("DEBUG")

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        message = ""
        output = None
        if is_debug:
            message = f"func={func.__name__} called with {args=}, {kwargs=}"

        try:
            output = func(*args, **kwargs)
            return output
        finally:
            if is_debug:
                print(f"{message}, returned {output=}")

    return wrapper
