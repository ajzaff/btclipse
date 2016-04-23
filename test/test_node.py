import unittest
import tables
import node


class TestNode(unittest.TestCase):

    def test_default_peers(self):
        self.assertEqual(node.Node().outpeers, 8)

    def test_default_newtable(self):
        self.assertEqual(node.Node().newtable, tables.NewTable())

    def test_default_triedtable(self):
        self.assertEqual(node.Node().triedtable, tables.TriedTable())

    def test_custom_peers(self):
        self.assertEqual(node.Node(outpeers=16).outpeers, 16)

    def test_custom_new_table(self):
        table = tables.NewTable(buckets=0)
        self.assertEqual(node.Node(triedtable=table).triedtable, table)

    def test_custom_tried_table(self):
        table = tables.TriedTable(buckets=0)
        self.assertEqual(node.Node(triedtable=table).triedtable, table)

    def test_init_len(self):
        self.assertEqual(len(node.Node()), 0)

    def test_nonzero_len(self):
        n = node.Node(outpeers=8)
        for i in range(5):
            n[i] = tables.PeerEntry(0)
        self.assertEqual(len(n), 5)

    def test_getitem_none(self):
        self.assertEqual(node.Node(outpeers=8)[0], None)

    def test_getitem_entry(self):
        n = node.Node(outpeers=8)
        e = tables.PeerEntry(0)
        n[0] = e
        self.assertEqual(n[0], e)

    def test_setitem_none_none(self):
        n = node.Node(outpeers=8)
        n[0] = None
        self.assertEqual(n[0], None)
        self.assertEqual(len(n), 0)

    def test_setitem_none_entry(self):
        n = node.Node(outpeers=8)
        e = tables.PeerEntry(0)
        n[0] = e
        self.assertEqual(n[0], e)
        self.assertEqual(len(n), 1)

    def test_setitem_entry_none(self):
        n = node.Node(outpeers=8)
        n[0] = tables.PeerEntry(0)
        n[0] = None
        self.assertEqual(n[0], None)
        self.assertEqual(len(n), 0)

    def test_delitem_none(self):
        n = node.Node(outpeers=8)
        del n[0]
        self.assertEqual(n[0], None)
        self.assertEqual(len(n), 0)

    def test_delitem_entry(self):
        n = node.Node(outpeers=8)
        n[0] = tables.PeerEntry(0)
        del n[0]
        self.assertEqual(n[0], None)
        self.assertEqual(len(n), 0)