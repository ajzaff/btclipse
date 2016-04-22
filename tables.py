class BaseTable(tuple):
    def __new__(cls, *args, **kwargs):
        return tuple(Bucket(slots=kwargs.get('slots')) for _ in range(kwargs.get('buckets')))


class NewTable(BaseTable):
    def __new__(cls, *args, **kwargs):
        return super(NewTable, cls).__new__(cls, buckets=kwargs.get('buckets', 256), slots=kwargs.get('slots', 64))


class TriedTable(BaseTable):
    def __new__(cls, *args, **kwargs):
        return super(TriedTable, cls).__new__(cls, buckets=kwargs.get('buckets', 64), slots=kwargs.get('slots', 64))


class Bucket(tuple):
    def __new__(cls, *args, **kwargs):
        return tuple(None for _ in range(kwargs.get('slots', 64)))


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