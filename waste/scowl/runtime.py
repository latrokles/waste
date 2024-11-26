from .reader import CharacterStream, Reader


class Runtime:
    def read_(self, src):
        return Reader(CharacterStream(src)).read_form()

    def eval_(self, expr):
        return expr

    def print_(self, form):
        match form:
            case str():
                return f'"{form}"'
            case _:
                return repr(form)

    def start(self):
        while True:
            print(self.print_(self.eval_(self.read_(input(">> ")))))
