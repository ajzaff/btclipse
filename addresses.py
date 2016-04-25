import numpy as np


class SimpleAddress(object):

    def __init__(self, group, ip):
        self._group = str(group)
        self._ip = str(ip)
        self._str = '%s:%s' % (self.group, self.ip)

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

    @staticmethod
    def randomaddress(rand=np.random, groups=None):
        group = rand.choice(groups) if groups else \
            rand.randint(1, 65536)
        ip = rand.randint(0, 65536)
        return SimpleAddress(group, ip)