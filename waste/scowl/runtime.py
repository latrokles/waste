import datetime
import decimal
import uuid

from .reader import CharacterStream, Reader


class Runtime:
    def read_(self, src):
        return Reader(CharacterStream(src)).read_form()

    def eval_(self, expr):
        return expr

    def print_(self, form):
        match form:
            case None:
                return "nil"
            case bool():
                return str(form).lower()
            case str():
                return f'"{form}"'
            case decimal.Decimal:
                return f"{form}M"
            case list():
                return "(" + " ".join(self.print_(f) for f in form) + ")"
            case tuple():
                return "[" + " ".join(self.print_(f) for f in form) + "]"
            case dict():
                return "{" + " ".join(f"{self.print_(k)} {self.print_(v)}" for k, v in form.items()) + "}"
            case datetime.datetime():
                return f'#datetime \"{form.strftime("%Y-%m-%dT%H:%M:%S%z")}\"'
            case datetime.date():
                return f'#date \"{form.strftime("%Y-%m-%d")}\"'
            case uuid.UUID():
                return f'#uuid "{form}"'
            case _:
                return repr(form)

    def start(self):
        while True:
            print(self.print_(self.eval_(self.read_(input(">> ")))))
