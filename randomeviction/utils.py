import hashlib


def hash(*inputs):
    preimage = ''.join(map(str, inputs))
    return int(hashlib.md5(preimage).hexdigest(), 16)


def triedbucket(addr, buckets=64):
    i = hash(addr) % 4
    return hash(addr.group, i) % buckets


def newbucket(my_addr, new_addr, buckets=256):
    i = hash(new_addr.group, my_addr.group) % 32
    return hash(new_addr.group, i) % buckets


def triedslot(addr, buckets=64, slots=64):
    pos = triedbucket(addr, buckets=buckets * slots)
    return pos / slots, pos % slots


def newslot(my_addr, new_addr, buckets=256, slots=64):
    pos = newbucket(my_addr, new_addr, buckets=buckets * slots)
    return pos / slots, pos % slots