import unittest
import tables


class TestNewTable(unittest.TestCase):

    def test_default_buckets(self):
        self.assertEqual(tables.NewTable().buckets, 256)

    def test_custom_buckets(self):
        self.assertEqual(tables.NewTable(buckets=5).buckets, 5)

    def test_default_slots(self):
        self.assertEqual(tables.NewTable()[0].slots, 64)

    def test_custom_slots(self):
        self.assertEqual(tables.NewTable(slots=2)[0].slots, 2)


class TestTriedTable(unittest.TestCase):

    def test_default_buckets(self):
        self.assertEqual(tables.TriedTable().buckets, 64)

    def test_custom_buckets(self):
        self.assertEqual(tables.TriedTable(buckets=10).buckets, 10)

    def test_default_slots(self):
        self.assertEqual(tables.TriedTable()[0].slots, 64)

    def test_custom_slots(self):
        self.assertEqual(tables.TriedTable(slots=10)[0].slots, 10)


class TestBucket(unittest.TestCase):

    def test_default_slots(self):
        self.assertEqual(tables.Bucket().slots, 64)

    def test_custom_slots(self):
        self.assertEqual(tables.Bucket(slots=2).slots, 2)


class TestEntry(unittest.TestCase):

    def test_default_timestamp(self):
        self.assertEqual(tables.TableEntry(0).timestamp, None)

    def test_property_ip(self):
        self.assertEqual(tables.TableEntry(0).ip, 0)

    def test_property_timestamp(self):
        self.assertEqual(tables.TableEntry(0, timestamp=1).timestamp, 1)

    def test_lt_entry(self):
        self.assertLess(tables.TableEntry(0, timestamp=1), tables.TableEntry(1, timestamp=2))

    def test_le_entry(self):
        self.assertLessEqual(tables.TableEntry(0, timestamp=1), tables.TableEntry(1, timestamp=1))

    def test_eq_entry(self):
        self.assertEqual(tables.TableEntry(0, timestamp=1), tables.TableEntry(0, timestamp=1))