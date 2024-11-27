import datetime
import decimal
import operator
import uuid

from waste.debug import debug

from .reader import CharacterStream, Reader
from .type import Condition, Keyword, Symbol


class Runtime:
    def __init__(self):
        self.env = {
            Symbol("+"): operator.add,
            Symbol("-"): operator.sub,
            Symbol("*"): operator.mul,
            Symbol("/"): operator.truediv,
            Symbol("upcase"): lambda s: s.upper(),
            Symbol("downcase"): lambda s: s.lower(),
            Symbol("symbol?"): lambda t: isinstance(t, Symbol),
            Symbol("keyword?"): lambda t: isinstance(t, Keyword),
            Symbol("list?"): lambda t: isinstance(t, list),
            Symbol("string?"): lambda t: isinstance(t, str),
            Symbol("number?"): lambda t: isinstance(t, int)
            or isinstance(t, float)
            or isinstance(t, decimal.Decimal),
            Symbol("nil?"): lambda t: t is None,
            Symbol("true?"): lambda t: t is True,
            Symbol("false?"): lambda t: t is False,
        }

    def read_(self, src):
        return Reader(CharacterStream(src)).read_form()

    def eval_(self, expr):
        debug(f"{expr = }")

        if isinstance(expr, Symbol):
            form = self.env.get(expr)
            if form is None:
                print(f"Unable to resolve Symbol `{expr}`!")
                return expr
            return form

        if not isinstance(expr, list):
            return expr

        # technically everything from here on out is a list
        sym, *rest = expr
        fn = self.eval_(sym)
        args = [self.eval_(a) for a in rest]
        return fn(*args)

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
                return (
                    "{"
                    + " ".join(
                        f"{self.print_(k)} {self.print_(v)}" for k, v in form.items()
                    )
                    + "}"
                )
            case datetime.datetime():
                return f'#datetime "{form.strftime("%Y-%m-%dT%H:%M:%S%z")}"'
            case datetime.date():
                return f'#date "{form.strftime("%Y-%m-%d")}"'
            case uuid.UUID():
                return f'#uuid "{form}"'
            case _:
                return repr(form)

    def start(self):
        while True:
            print(self.print_(self.eval_(self.read_(input(">> ")))))
