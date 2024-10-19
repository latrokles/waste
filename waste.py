def is_blank(s):
    return s == '' or s.isspace()


def is_not_blank(s):
    return not is_blank()


class Objeckt:
    def metadata(self):
        return self._metadata


class Symbol(Objeckt):
    def __init__(self, name, namespace=None, metadata=None):
        self.name = name
        self.namespace = namespace
        self._metadata = metadata

    @property
    def ns(self):
        return self.namespace

    def __eq__(self, rhs):
        if self is rhs:
            return True

        if not isinstance(rhs, Symbol):
            return False

        return (self.name == rhs.name) and (self.ns == rhs.ns)


class Keyword(Symbol):
    pass


class String(Objeckt):
    def __init__(self, value):
        self.value = value


class Integer(Objeckt):
    def __init__(self, value):
        self.value = value


class Fn(Objeckt):
    def invoke(self, *args):
        pass


class CharStream:

    def __init__(self, txt):
        self.txt = txt
        self.idx = 0
        self.row = 1
        self.col = 1

    @property
    def length(self):
        return len(self.txt)

    @property
    def position(self):
        return self.row, self.col

    def read(self):
        if self.idx >= self.length:
            return ""

        char = self.txt[self.idx]
        self.idx += 1
        self.col += 1

        if char == '\n':
            self.row += 1
            self.col = 1

        return char

    def peek(self):
        return self.txt[self.idx]

    def skip(self):
        self.read()
        return self


class StringReader(Fn):
    def invoke(self, *args):
        chars = []
        reader, *rest = args

        # consume opening quote
        reader.read1()

        # read characters until we reach the closing quote
        while (char := reader.read1()) != "'":
            if char == "":
                raise RuntimeError("found EOF while reading string, make this a ReaderException")
            chars.append(char)

        # consume the closing quote
        reader.read1()
        return "".join(chars)

class BlockReader(Fn):
    def invoke(self, *args):
        pass


class UnmatchedDelimiterReader(Fn):
    def invoke(self, *args):
        pass


class DispatchReader(Fn):
    def invoke(self, *args):
        pass


class SingleLineCommentReader(Fn):
    def invoke(self, *args):
        pass


class ListReader(Fn):
    def invoke(self, *args):
        pass


class MapReader(Fn):
    def invoke(self, *args):
        pass


class Reader:
    READERS = {
        "'": StringReader(),
        '[': BlockReader(),
        ']': UnmatchedDelimiterReader(),
        '#': DispatchReader(),
        ';': SingleLineCommentReader(),
    }

    DISPATCH_READERS = {
        '[': ListReader(),
        '{': MapReader(),
    }

    def __init__(self, datastream):
        self.data = datastream

    def read(self):
        char = self.read1()

        while is_blank(char):
            char = self.read1()

    def skip_blankspace(self):
        pass

    def read1(self):
        return self.data.read()

