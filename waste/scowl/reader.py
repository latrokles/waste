import datetime
import decimal
import re
import uuid

from .type import Condition, Keyword, Symbol


BLANKSPACE_REGEX = re.compile(r"[\s,]")
NUMBER_REGEX = re.compile(r"[0-9\-]")
CANDIDATE_NUMBER_CHAR_REGEX = re.compile(r"[0-9A-Fa-fxM\-\._]")
HEX_INT_REGEX = re.compile(r"^-?0[xX][0-9a-fA-F_]*$")
INT_REGEX = re.compile(r"^-?\d+(_\d+)*$")
FLOAT_REGEX = re.compile(r"^-?\d+(_\d+)*(\.\d+(_\d+)*)?([eE]-?\d+(_\d+)*)?$")
DECIMAL_REGEX = re.compile(r"^-?\d+(_\d+)*(\.\d+(_\d+)*)?([eE]-?\d+(_\d+)*)?M$")
SYMBOL_START_REGEX = re.compile(r"u(\w)|\w|\=|\+|\*|\.|\?|<|>|!|%|&|-|_|")
SYMBOL_CHAR_REGEX = re.compile(r"u(\w)|\w|\=|\+|\*|\.|\?|/|<|>|!|%|&|-|_|:")

DELIMITERS = "(){}[];\n "
EOF = Symbol("#EOF#", "reader")


class CharacterStream:
    def __init__(self, text):
        self.txt = text
        self.pos = 0
        self.row = 1
        self.col = 1
        self.prev_col = 1

    @property
    def length(self):
        return len(self.txt)

    @property
    def location(self):
        return self.row, self.col

    def peek(self):
        if self.pos >= self.length:
            return ""
        return self.txt[self.pos]

    def read(self):
        char = self.peek()
        self._advance_position(char)
        return char

    def step_back(self):
        self.pos -= 1
        self.col = self.prev_col
        self.prev_col -= 1

        if self.txt[self.pos] == "\n":
            self.row -= 1

    def _advance_position(self, char):
        if char == "":
            return

        self.pos += 1
        self.prev_col = self.col
        self.col += 1

        if char == "\n":
            self.row += 1
            self.col = 1


# reader functions
def _read_after_blankspace(reader):
    reader.skip_blankspace()
    return reader.read_form()


def _read_string(reader):
    chars = []
    reader.read1()  # consume opening quotation mark

    while (c := reader.read1()) != '"':
        if c == "":
            return Condition(
                Keyword("ReaderError"), "Unterminated string. Reached EOF!"
            )
        chars.append(c)
    return "".join(chars)


def _read_number(reader):
    chars = []

    while CANDIDATE_NUMBER_CHAR_REGEX.match(reader.peek()):
        chars.append(reader.read1())

    candidate = "".join(chars)

    if INT_REGEX.fullmatch(candidate):
        return int(candidate)

    if HEX_INT_REGEX.fullmatch(candidate):
        return int(candidate, 16)

    if DECIMAL_REGEX.fullmatch(candidate):
        return decimal.Decimal(candidate[:-1])

    if FLOAT_REGEX.fullmatch(candidate):
        return float(candidate)

    return Condition(Keyword("ReaderError"), f"Invalid number `{candidate}`!")


def _read_collection(reader, terminator):
    form = []
    reader.read1()  # consume opening

    while reader.peek() != terminator:
        form.append(reader.read_form())

    reader.read1()  # consume closing
    return form


def _read_list(reader):
    return _read_collection(reader, ")")


def _read_tuple(reader):
    return tuple(_read_collection(reader, "]"))


def _read_map(reader):
    form = _read_collection(reader, "}")
    i = iter(form)
    return dict(zip(i, i))


def _read_data(reader):
    return reader.read_data()


def _read_comment(reader):
    while reader.read1() not in ("\n", ""):
        pass
    return reader.read_form()


def _read_keyword(reader):
    def valid_keyword_char(c):
        return SYMBOL_CHAR_REGEX.match(c) and (c not in "[]{}()")

    chars = []
    while valid_keyword_char(c := reader.read1()):
        chars.append(c)

    candidate = "".join(chars[1:])
    if "/" in candidate:
        namespace, *rest = candidate.split("/")
        return Keyword("".join(rest), namespace)
    return Keyword(candidate)


def _read_symbol(reader):
    def valid_symbol_char(c):
        return SYMBOL_CHAR_REGEX.match(c) and (c not in "[]{}()")

    chars = []
    while valid_symbol_char(reader.peek()):
        chars.append(reader.read1())
    candidate = "".join(chars)

    if candidate == "nil":
        return None

    if candidate == "true":
        return True

    if candidate == "false":
        return False

    if "/" in candidate:
        namespace, *rest = candidate.split("/")
        return Symbol("".join(rest), namespace)
    return Symbol(candidate)


# list of (predicate, reader_fn) tuples
FORM_READERS = [
    (lambda c: BLANKSPACE_REGEX.match(c), _read_after_blankspace),
    (lambda c: c == '"', _read_string),
    (lambda c: NUMBER_REGEX.match(c), _read_number),
    (lambda c: c == "(", _read_list),
    (lambda c: c == "[", _read_tuple),
    (lambda c: c == "{", _read_map),
    (lambda c: c == "#", _read_data),
    (lambda c: c == ";", _read_comment),
    (lambda c: c == ":", _read_keyword),
    (lambda c: SYMBOL_START_REGEX.match(c), _read_symbol),
]


def __read_literal(reader, func, reader_error_message):
    try:
        literal = reader.read_form()
        return func(literal)
    except (ValueError, AttributeError) as e:
        return Condition(
            Keyword("ReaderError"),
            reader_error_message.format(literal),
            meta={"cause": e.args[0]},
        )


def _read_date(reader):
    return __read_literal(
        reader,
        lambda lit: datetime.datetime.strptime(lit, "%Y-%m-%d").date(),
        "Unable to read date {}!",
    )


def _read_datetime(reader):
    return __read_literal(
        reader,
        lambda lit: datetime.datetime.strptime(lit, "%Y-%m-%dT%H:%M:%S%z"),
        "Unable to read datetime {}!",
    )


def _read_epoch_seconds(reader):
    return __read_literal(
        reader,
        lambda lit: datetime.datetime.fromtimestamp(lit, tz=datetime.timezone.utc),
        "Unable to read timestamp `{}`!",
    )


def _read_epoch_millis(reader):
    return __read_literal(
        reader,
        lambda lit: datetime.datetime.fromtimestamp(
            lit / 1_000, tz=datetime.timezone.utc
        ),
        "Unable to read timestamp `{}`!",
    )


def _read_uuid(reader):
    return __read_literal(
        reader,
        lambda lit: uuid.UUID(lit),
        "Unable to read uuid `{}`",
    )


DATA_READERS = {
    "#date": _read_date,
    "#datetime": _read_datetime,
    "#ts-secs": _read_epoch_seconds,
    "#ts-millis": _read_epoch_millis,
    "#uuid": _read_uuid,
}


class Reader:
    def __init__(self, stream, form_readers=None, data_readers=None):
        self.stream = stream
        self.form_readers = form_readers or FORM_READERS
        self.data_readers = data_readers or DATA_READERS
        self.eof = EOF

    def read_form(self):
        char = self.peek()

        if char == "":
            return self.eof

        for pred, reader_fn in self.form_readers:
            if pred(char):
                return reader_fn(self)

        return Condition(Keyword("ReaderError"), "No Reader for `{char=}`!")

    def read_data(self):
        key = self.read_until_blankspace()
        data_reader = self.data_readers.get(key)

        if not data_reader:
            return Condition(
                Keyword("ReaderError"), f"No suitable data reader found for `{key}`!"
            )
        self.skip_blankspace()
        return data_reader(self)

    def peek(self):
        return self.stream.peek()

    def read1(self):
        return self.stream.read()

    def read_until_blankspace(self):
        chars = []
        while not BLANKSPACE_REGEX.match(c := self.read1()):
            chars.append(c)
        return "".join(chars)

    def read_until_delimiter(self):
        chars = []
        while self.peek() not in DELIMITERS:
            chars.append(self.read1())
        return "".join(chars)

    def skip_blankspace(self):
        while BLANKSPACE_REGEX.match(self.peek()):
            self.read1()

    def back(self):
        return self.stream.step_back()
