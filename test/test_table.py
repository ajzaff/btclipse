import unittest
import tables


class TestTable(unittest.TestCase):

    def test_default_buckets(self):
        assert len(tables.NewTable()) == 256

    def test_custom_buckets(self):
        assert len(tables.NewTable(buckets=100)) == 100

    def test_default_slots(self):
        assert len(tables.NewTable()[0]) == 64

    def test_custom_slots(self):
        assert len(tables.NewTable(slots=10)[0]) == 10


class TestTriedTable(unittest.TestCase):

    def test_default_buckets(self):
        assert len(tables.TriedTable()) == 64

    def test_custom_buckets(self):
        assert len(tables.TriedTable(buckets=10)) == 10

    def test_default_slots(self):
        assert len(tables.TriedTable()[0]) == 64

    def test_custom_slots(self):
        assert len(tables.TriedTable(slots=10)[0]) == 10


class TestBucket(unittest.TestCase):

    def test_default_slots(self):
        assert len(tables.Bucket()) == 64

    def test_custom_slots(self):
        assert len(tables.Bucket(slots=2)) == 2


class TestEntry(unittest.TestCase):

    def test_default_timestamp(self):
        assert tables.TableEntry(0).timestamp is None

    def test_property_ip(self):
        assert tables.TableEntry(0).ip == 0

    def test_property_timestamp(self):
        assert tables.TableEntry(0, timestamp=1).timestamp == 1

    def test_lt(self):
        assert tables.TableEntry(0, timestamp=1) < tables.TableEntry(1, timestamp=2)

    def test_le(self):
        assert tables.TableEntry(0, timestamp=1) <= tables.TableEntry(1, timestamp=1)

    def test_ge(self):
        assert tables.TableEntry(0, timestamp=2) >= tables.TableEntry(1, timestamp=2)

    def test_gt(self):
        assert tables.TableEntry(0, timestamp=2) > tables.TableEntry(1, timestamp=1)