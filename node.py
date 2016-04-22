import tables


class Node(tuple):

    def __init__(self, *args, **kwargs):
        super(Node, self).__init__(*args, **kwargs)
        self._newtable = kwargs.get('newtable', tables.NewTable())
        self._triedtable = kwargs.get('triedtable', tables.TriedTable())

    def __new__(self, **kwargs):
        return tuple(None for _ in range(kwargs.get('peers', 8)))

    @property
    def newtable(self):
        return self._newtable

    @property
    def triedtable(self):
        return self._triedtable