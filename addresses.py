class SimpleAddress(object):

    def __init__(self, group, ip):
        self._group = group
        self._ip = ip
        self._str = '%d:%d' % (self.group, self.ip)

    @property
    def group(self):
        return self._group

    @property
    def ip(self):
        return self._ip

    def __str__(self):
        return self._str

    def __eq__(self, other):
        return self.ip == other.ip and \
               self.group == other.group