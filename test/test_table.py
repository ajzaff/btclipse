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
                table[i][j] = tables.PeerEntry(0)
        self.assertEqual(len(table), 25)

    def test_get_item(self):
        table = tables.BaseTable(1, 1)
        table[0][0] = tables.PeerEntry(0)
        self.assertEqual(table[0], table.elems[0])

    def test_get_item_indexerror(self):
        with self.assertRaises(IndexError):
            tables.BaseTable(1, 1).__getitem__(2)

    def test_delitem_empty(self):
        table = tables.BaseTable(1, 1)
        del table[0]
        self.assertEqual(table[0], tables.Bucket(slots=1))
        self.assertEqual(len(table), 0)

    def test_delitem_nonempty(self):
        table = tables.BaseTable(1, 1)
        table[0][0] = tables.PeerEntry(0)
        del table[0]
        self.assertEqual(table[0], tables.Bucket(slots=1))
        self.assertEqual(len(table), 0)

    def test_eq_equal(self):
        table1 = tables.BaseTable(10, 10)
        table2 = tables.BaseTable(10, 10)
        for i in range(5):
            for j in range(10):
                table1[i][j] = tables.PeerEntry(i * j)
                table2[i][j] = tables.PeerEntry(i * j)
        self.assertEqual(table1, table2)

    def test_eq_nonequal(self):
        table1 = tables.BaseTable(10, 10)
        table2 = tables.BaseTable(10, 10)
        for i in range(5):
            for j in range(10):
                table1[i][j] = tables.PeerEntry(i * j)
                table2[i][j] = tables.PeerEntry(i + j)
        self.assertNotEqual(table1, table2)


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
            bucket[i] = tables.PeerEntry(0)
        self.assertEqual(len(bucket), 5)

    def test_clear(self):
        bucket = tables.Bucket(slots=10)
        for i in range(10):
            bucket[i] = tables.PeerEntry(0)
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
        bucket[0] = tables.PeerEntry(0)
        self.assertEqual(bucket[0], bucket.elems[0])

    def test_set_item_none_to_none(self):
        bucket = tables.Bucket(slots=1)
        bucket[0] = None
        self.assertEqual(bucket[0], None)
        self.assertEqual(len(bucket), 0)

    def test_set_item_none_to_entry(self):
        bucket = tables.Bucket(slots=1)
        entry = tables.PeerEntry(0)
        bucket[0] = entry
        self.assertEqual(bucket[0], entry)
        self.assertEqual(len(bucket), 1)

    def test_set_item_entry_to_none(self):
        bucket = tables.Bucket(slots=1)
        bucket[0] = tables.PeerEntry(0)
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
        bucket[0] = tables.PeerEntry(0)
        del bucket[0]
        self.assertEqual(bucket[0], None)
        self.assertEqual(len(bucket), 0)

    def test_eq_equal(self):
        table1 = tables.BaseTable(10, 10)
        table2 = tables.BaseTable(10, 10)
        for i in range(5):
            for j in range(10):
                table1[i][j] = tables.PeerEntry(i * j)
                table2[i][j] = tables.PeerEntry(i * j)
        self.assertEqual(table1, table2)

    def test_eq_nonequal(self):
        bucket1 = tables.Bucket(slots=10)
        bucket2 = tables.Bucket(slots=10)
        for i in range(5):
            bucket1[i] = tables.PeerEntry(i)
            bucket2[i] = tables.PeerEntry(-i)
        self.assertNotEqual(bucket1, bucket2)


class TestEntry(unittest.TestCase):

    def test_default_timestamp(self):
        self.assertEqual(tables.PeerEntry(0).timestamp, None)

    def test_property_ip(self):
        self.assertEqual(tables.PeerEntry(0).ip, 0)

    def test_property_timestamp(self):
        self.assertEqual(tables.PeerEntry(0, timestamp=1).timestamp, 1)

    def test_lt_entry(self):
        self.assertLess(tables.PeerEntry(0, timestamp=1), tables.PeerEntry(1, timestamp=2))

    def test_le_entry(self):
        self.assertLessEqual(tables.PeerEntry(0, timestamp=1), tables.PeerEntry(1, timestamp=1))

    def test_eq_entry(self):
        self.assertEqual(tables.PeerEntry(0, timestamp=1), tables.PeerEntry(0, timestamp=1))