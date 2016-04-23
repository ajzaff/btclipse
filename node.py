import tables


class Node(object):

    def __init__(self, **kwargs):
        self._newtable = kwargs.get('newtable', tables.NewTable())
        self._triedtable = kwargs.get('triedtable', tables.TriedTable())
        self._outpeers = kwargs.get('outpeers', 8)
        self._peers = [None for _ in range(self.outpeers)]
        self._len = 0

    def __len__(self):
        return self._len

    def __getitem__(self, item):
        return self._peers[item]

    def __setitem__(self, key, value):
        if not self._peers[key] and value:
            self._len += 1
        elif self._peers[key] and not value:
            self._len -= 1
        self._peers[key] = value

    def __delitem__(self, key):
        if self._peers[key]:
            self._len -= 1
        self._peers[key] = None

    def clear(self):
        for i in range(self.outpeers):
            self._peers[i] = None
        self._len = 0

    @property
    def outpeers(self):
        return self._outpeers

    @property
    def peers(self):
        return tuple(self._peers)

    @property
    def newtable(self):
        return self._newtable

    @property
    def triedtable(self):
        return self._triedtable

    @property
    def rho(self):
        return len(self.triedtable) / len(self.newtable)

    @property
    def omega(self):
        return self._len