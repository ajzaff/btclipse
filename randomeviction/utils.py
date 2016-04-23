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
