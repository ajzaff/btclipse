import unittest
import tables


class TestBaseTable(unittest.TestCase):

    def test_default_buckets(self):
        self.assertEqual(tables.NewTable().buckets, 256)

    def test_custom_buckets(self):
        self.assertEqual(tables.NewTable(buckets=5).buckets, 5)

    def test_default_slots(self):
        self.assertEqual(tables.NewTable()[0].slots, 64)

    def test_custom_slots(self):
        self.assertEqual(tables.NewTable(slots=2)[0].slots, 2)

    def test_init_len(self):
        self.assertEqual(len(tables.BaseTable(1, 1)), 0)

    def test_nonzero_len(self):
        table = tables.BaseTable(buckets=10, slots=10)
        for i in range(5):
            for j in range(5):
                table[i][j] = tables.TableEntry(0)
        self.assertEqual(len(table), 25)

    def test_get_item(self):
        table = tables.BaseTable(1, 1)
        table[0][0] = tables.TableEntry(0)
        self.assertEqual(table[0], table.elems[0])

    def test_get_item_indexerror(self):
        with self.assertRaises(IndexError):
            tables.BaseTable(1, 1).__getitem__(2)


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

    def test_init_len(self):
        self.assertEqual(len(tables.Bucket(slots=1)), 0)

    def test_nonzero_len(self):
        bucket = tables.Bucket(slots=10)
        for i in range(5):
            bucket[i] = tables.TableEntry(0)
        self.assertEqual(len(bucket), 5)

    def test_clear(self):
        bucket = tables.Bucket(slots=10)
        for i in range(10):
            bucket[i] = tables.TableEntry(0)
        bucket.clear()
        for i in range(10):
            self.assertEqual(bucket[i], None)
        self.assertEqual(len(bucket), 0)

    def test_property_elems(self):
        bucket = tables.Bucket()
        self.assertEqual(bucket.elems, tuple(bucket._elems))

    def test_getitem_indexerror(self):
        with self.assertRaises(IndexError):
            tables.Bucket(slots=1).__getitem__(1)

    def test_getitem_empty(self):
        self.assertEqual(tables.Bucket(slots=1)[0], None)

    def test_getitem_entry(self):
        bucket = tables.Bucket(slots=2)
        bucket[0] = tables.TableEntry(0)
        self.assertEqual(bucket[0], bucket.elems[0])

    def test_set_item_none_to_none(self):
        bucket = tables.Bucket(slots=1)
        bucket[0] = None
        self.assertEqual(bucket[0], None)
        self.assertEqual(len(bucket), 0)

    def test_set_item_none_to_entry(self):
        bucket = tables.Bucket(slots=1)
        entry = tables.TableEntry(0)
        bucket[0] = entry
        self.assertEqual(bucket[0], entry)
        self.assertEqual(len(bucket), 1)

    def test_set_item_entry_to_none(self):
        bucket = tables.Bucket(slots=1)
        bucket[0] = tables.TableEntry(0)
        bucket[0] = None
        self.assertEqual(bucket[0], None)
        self.assertEqual(len(bucket), 0)

    def test_del_item_none(self):
        bucket = tables.Bucket(slots=1)
        del bucket[0]
        self.assertEqual(bucket[0], None)
        self.assertEqual(len(bucket), 0)

    def test_del_item_entry(self):
        bucket = tables.Bucket(slots=1)
        bucket[0] = tables.TableEntry(0)
        del bucket[0]
        self.assertEqual(bucket[0], None)
        self.assertEqual(len(bucket), 0)


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