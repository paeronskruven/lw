class BaseSource:

    def query(self, key):
        raise NotImplementedError


sources = []


def query(key):
    for source in sources:
        yield source.query(key)
