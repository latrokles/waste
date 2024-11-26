from .type import Condition, Symbol


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
def _read_string(reader):
    chars = []
    reader.read1()  # consume opening quotation mark

    while (c := reader.read1()) != '"':
        if c == "":
            return Condition("ReaderError", "Unterminated string. At EOF!")
        chars.append(c)
    return "".join(chars)


# list of (predicate, reader_fn) tuples
FORM_READERS = [(lambda c: c == '"', _read_string)]
DATA_READERS = {}


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

        return Condition("ReaderError", "No Reader for `{char=}`!")

    def peek(self):
        return self.stream.peek()

    def read1(self):
        return self.stream.read()

    def back(self):
        return self.stream.step_back()
