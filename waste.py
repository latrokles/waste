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



class Reader:
    pass

