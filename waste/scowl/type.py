"""scowl uses as many of the python types as possible in order to make interop "easier". this has some implications if scowl were to be implemented on a different substrate, but this is mainly a toy so... :shrugh:!


nil -> None
true -> True
false -> False
string -> str
integer -> int
float -> float or Decimal ("0.5" or "0.5M")

list -> list ... (1 2 3).. a quoted list \(1 2 3)
tuple -> tuple ... [ 1 2 3 ] ... might make this a vector type ?
map -> dict ... {k1 v1 k2 v2}
set -> set ... #{v1 v2 v3}

in addition to the above, scowl defines:

symbols -> #'package/name
keywords -> :name  or :person/name

and...

functions.. tbd
"""

from __future__ import annotations
from dataclasses import dataclass, field
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class Symbol:
    val: str
    pkg: str
    meta: [dict[str, Form]] = field(default_factory=dict)

    def __hash__(self):
        return hash((self.val, self.pkg))

    def __eq__(self, rhs):
        if not isinstance(rhs, Symbol):
            return False

        return (self.val == rhs.val) and (self.pkg == rhs.pkg)

    def __repr__(self):
        return f"#'{self.pkg}/{self.val}"


@dataclass(frozen=True, slots=True)
class Keyword:
    val: str
    pkg: str | None = None

    def __hash__(self):
        if self.pkg:
            return hash((self.val, self.pkg))
        return hash(self.val)

    def __eq__(self, rhs):
        if not isinstance(rhs, Keyword):
            return False

        if self.pkg:
            return (self.val == rhs.val) and (self.pkg == rhs.pkg)
        return self.val == rhs.val

    def __repr__(self):
        if self.pkg:
            return f":{self.pkg}/{self.val}"
        return f":{self.val}"


@dataclass(frozen=True, slots=True)
class Condition:
    key: str
    val: str
    meta: dict[str, Form] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class Fn:
    pass


Form = (
    None
    | bool
    | str
    | int
    | float
    | Decimal
    | tuple
    | list
    | dict
    | set
    | Symbol
    | Keyword
    | Condition
    | Fn
)
