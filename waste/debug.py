import functools
import os


def debugmethod(func):
    is_debug = os.getenv("DEBUG")

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        message = ""

        if is_debug:
            message = f"func={func.__name__} called with {args=}, {kwargs=}"

        output = func(self, *args, **kwargs)

        if is_debug:
            print(f"{message}, returned {output=}")

        return output
    return wrapper


