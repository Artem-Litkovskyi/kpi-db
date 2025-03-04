import unittest

from lab2.btree import *


TEST_NODES = BTreeNode(
    False,
    [19],
    [
        BTreeNode(
            False,
            [5, 13],
            [
                BTreeNode(
                    True,
                    [2, 3],
                    [['2'], ['3']]
                ),
                BTreeNode(
                    True,
                    [5, 7, 8],
                    [['5'], ['7'], ['8']]
                ),
                BTreeNode(
                    True,
                    [14, 16],
                    [['14'], ['16']]
                )
            ]
        ),
        BTreeNode(
            False,
            [24, 30],
            [
                BTreeNode(
                    True,
                    [19, 20, 22],
                    [['19'], ['20'], ['22']]
                ),
                BTreeNode(
                    True,
                    [24, 27, 29],
                    [['24'], ['27', '2 7'], ['29']]
                ),
                BTreeNode(
                    True,
                    [33, 34, 38, 39],
                    [['33'], ['34'], ['38'], ['39']]
                )
            ]
        )
    ]
)


def get_key_for_value(value: str):
    return int(value.replace(' ', ''))


def test_key_hash_provider(key: int):
    return key


class SearchTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tree = BTree(test_key_hash_provider, 2)
        cls.tree.root = TEST_NODES

    def test_existing(self):
        value = '29'
        key = get_key_for_value(value)
        self.assertIn(value, SearchTest.tree.search(key))

    def test_common_key(self):
        values = ['27', '2 7']
        for value in values:
            key = get_key_for_value(value)
            self.assertIn(value, SearchTest.tree.search(key))

    def test_not_existing(self):
        value = '28'
        key = get_key_for_value(value)
        self.assertEqual(0, len(SearchTest.tree.search(key)))

    def test_search_less(self):
        expected_values = ['2', '3', '5']
        actual_values = SearchTest.tree.search_less(get_key_for_value('7'))
        for v in expected_values:
            self.assertIn(v, actual_values)

    def test_search_less_not_existing(self):
        expected_values = ['2', '3', '5']
        actual_values = SearchTest.tree.search_less(get_key_for_value('6'))
        for v in expected_values:
            self.assertIn(v, actual_values)

    def test_search_greater(self):
        expected_values = ['24', '27', '2 7', '29', '33', '34', '38', '39']
        actual_values = SearchTest.tree.search_greater(get_key_for_value('22'))
        for v in expected_values:
            self.assertIn(v, actual_values)

    def test_search_greater_not_existing(self):
        expected_values = ['24', '27', '2 7', '29', '33', '34', '38', '39']
        actual_values = SearchTest.tree.search_greater(get_key_for_value('23'))
        for v in expected_values:
            self.assertIn(v, actual_values)


class InsertionTest(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.tree = BTree(test_key_hash_provider, 2)

    def assert_insertion(self, values):
        for value in values:
            key = get_key_for_value(value)
            InsertionTest.tree.insert(key, value)
            self.assertIn(value, InsertionTest.tree.search(key))

    def test_insert(self):
        with self.subTest('Insert into the root node'):
            self.assert_insertion(('59','23','7', '97'))

        with self.subTest('Insert that causes the root (leaf) to split, creating a new root node'):
            self.assert_insertion(('73',))

        with self.subTest('Insert into the left and right subtrees'):
            self.assert_insertion(('67', '19'))

        with self.subTest('Insert that causes the right leaf to split, adding a new key to the root'):
            self.assert_insertion(('79',))

        with self.subTest('Insert another value with a key that is already in the tree'):
            self.assert_insertion(('5 9',))

        with self.subTest('Inserts that cause the root (not leaf) to split, creating a new root node'):
            self.assert_insertion(('100', '101', '102', '103', '104', '105'))

class DeletionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tree = BTree(test_key_hash_provider, 2)
        cls.tree.root = TEST_NODES

    def assert_deletion(self, values):
        for value in values:
            key = get_key_for_value(value)
            DeletionTest.tree.delete(key, value)
            self.assertNotIn(value, DeletionTest.tree.search(key))

    def test_deletion(self):
        with self.subTest('Delete one of values with the same hash'):
            self.assert_deletion(('2 7',))

        with self.subTest('Delete that leaves enough keys'):
            self.assert_deletion(('7',))

        # with self.subTest('Delete that doesn\'t leave enough keys'):
        #     self.assert_deletion(('3',))


if __name__ == '__main__':
    unittest.main()
