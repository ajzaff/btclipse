import hashlib


def hash(x):
    return int(hashlib.md5(str(x)).hexdigest(), 16)