import unittest
from btree import *


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
                    ['2', '3']
                ),
                BTreeNode(
                    True,
                    [5, 7, 8],
                    ['5', '7', '8']
                ),
                BTreeNode(
                    True,
                    [14, 16],
                    ['14', '16']
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
                    ['19', '20', '22']
                ),
                BTreeNode(
                    True,
                    [24, 27, 27, 29],
                    ['24', '27', '2 7', '29']
                ),
                BTreeNode(
                    True,
                    [33, 34, 38, 39],
                    ['33', '34', '38', '39']
                )
            ]
        )
    ]
)


def test_key_provider(value: str):
    return int(value.replace(' ', ''))


class SearchTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tree = BTree(test_key_provider, 2)
        cls.tree.root = TEST_NODES
    def test_existing(self):
        value = '29'
        self.assertEqual([value], SearchTest.tree.search(value))

    def test_common_key(self):
        values = ['27', '2 7']
        for value in values:
            self.assertIn(value, SearchTest.tree.search(value))

    def test_not_existing(self):
        self.assertEqual([], SearchTest.tree.search('28'))

    def test_search_lower(self):
        expected_values = ['2', '3', '5']
        actual_values = SearchTest.tree.search_lower('7')
        for v in expected_values:
            self.assertIn(v, actual_values)

    def test_search_lower_not_existing(self):
        expected_values = ['2', '3', '5']
        actual_values = SearchTest.tree.search_lower('6')
        for v in expected_values:
            self.assertIn(v, actual_values)

    def test_search_greater(self):
        expected_values = ['24', '27', '2 7', '29', '33', '34', '38', '39']
        actual_values = SearchTest.tree.search_greater('22')
        for v in expected_values:
            self.assertIn(v, actual_values)

    def test_search_greater_not_existing(self):
        expected_values = ['24', '27', '2 7', '29', '33', '34', '38', '39']
        actual_values = SearchTest.tree.search_greater('23')
        for v in expected_values:
            self.assertIn(v, actual_values)


class InsertionTest(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.tree = BTree(test_key_provider, 2)

    def insertion(self, values):
        for value in values:
            InsertionTest.tree.insert(value)
            self.assertIn(value, InsertionTest.tree.search(value))

    def test_insert(self):
        with self.subTest('Insert into the root node'):
            self.insertion(('59','23','7', '97'))

        with self.subTest('Insert that causes the root node to split'):
            self.insertion(('73',))

        with self.subTest('Insert into left and right subtrees'):
            self.insertion(('67', '19'))

        with self.subTest('Insert that causes the right subtree to split'):
            self.insertion(('79',))

        with self.subTest('Insert another value with a key that is already in the tree'):
            self.insertion(('5 9',))


if __name__ == '__main__':
    unittest.main()
