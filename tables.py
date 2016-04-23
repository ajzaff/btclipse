class BaseTable(object):

    def __init__(self, buckets, slots):
        self._buckets = buckets
        self._slots = slots
        self._elems = [Bucket(slots=slots)
                       for _ in range(buckets)]

    def __len__(self):
        return sum(map(len, self.elems))

    def __getitem__(self, item):
        return self._elems[item]

    def __delitem__(self, key):
        self._elems[key].clear()

    def __eq__(self, other):
        return self.slots == other.slots and \
            self.buckets == other.buckets and \
            self.elems == other.elems

    @property
    def elems(self):
        return tuple(self._elems)

    @property
    def buckets(self):
        return self._buckets

    @property
    def slots(self):
        return self._slots


class NewTable(BaseTable):
    def __init__(cls, **kwargs):
        super(NewTable, cls).__init__(
            buckets=kwargs.get('buckets', 256),
            slots=kwargs.get('slots', 64))


class TriedTable(BaseTable):
    def __init__(cls, **kwargs):
        super(TriedTable, cls).__init__(
            buckets=kwargs.get('buckets', 64),
            slots=kwargs.get('slots', 64))


class Bucket(object):
    def __init__(self, **kwargs):
        self._slots = kwargs.get('slots', 64)
        self._elems = [None for _ in range(self.slots)]
        self._len = 0

    def __len__(self):
        return self._len

    def __getitem__(self, item):
        return self._elems[item]

    def __setitem__(self, key, value):
        if not self._elems[key] and value:
            self._len += 1
        elif self._elems[key] and not value:
            self._len -= 1
        self._elems[key] = value

    def __delitem__(self, key):
        if self._elems[key]:
            self._len -= 1
        self._elems[key] = None

    def __eq__(self, other):
        return self.slots == other.slots and \
            self.elems == other.elems

    def clear(self):
        for i in range(self.slots):
            self._elems[i] = None
        self._len = 0

    @property
    def elems(self):
        return tuple(self._elems)

    @property
    def slots(self):
        return self._slots


class PeerEntry(object):
    def __init__(self, ip, timestamp=None):
        self._ip = ip
        self._timestamp = timestamp

    @property
    def ip(self):
        return self._ip

    @property
    def timestamp(self):
        return self._timestamp

    def __lt__(self, other):
        return self.timestamp < other.timestamp

    def __le__(self, other):
        return self.timestamp <= other.timestamp

    def __eq__(self, other):
        return self.ip == other.ip and \
               self.timestamp == other.timestamp