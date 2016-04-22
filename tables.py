class BaseTable(tuple):

    def __init__(self, **kwargs):
        super(BaseTable, self).__init__()
        self._buckets = super(BaseTable, self).__len__()

    def __new__(cls, *args, **kwargs):
        return super(BaseTable, cls).__new__(
            cls,
            tuple(Bucket(slots=kwargs.get('slots')) for _ in range(kwargs.get('buckets'))))

    def __len__(self):
        return sum(map(len, self))

    @property
    def buckets(self):
        return self._buckets


class NewTable(BaseTable):
    def __new__(cls, *args, **kwargs):
        return super(NewTable, cls).__new__(cls, buckets=kwargs.get('buckets', 256), slots=kwargs.get('slots', 64))


class TriedTable(BaseTable):
    def __new__(cls, *args, **kwargs):
        return super(TriedTable, cls).__new__(cls, buckets=kwargs.get('buckets', 64), slots=kwargs.get('slots', 64))


class Bucket(tuple):

    def __init__(self, **kwargs):
        super(Bucket, self).__init__()
        self._slots = super(Bucket, self).__len__()

    def __new__(cls, *args, **kwargs):
        return super(Bucket, cls).__new__(
            cls,
            tuple(None for _ in range(kwargs.get('slots', 64))))

    def __len__(self):
        return sum(map(lambda e: 1 if e is not None else 0, self))

    @property
    def slots(self):
        return self._slots


class TableEntry(object):
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
        return self.ip == other.ip and self.timestamp == other.timestamp