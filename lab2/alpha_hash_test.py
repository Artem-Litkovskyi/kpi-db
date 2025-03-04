import unittest
from alpha_hash import *


class MyTestCase(unittest.TestCase):
    def setUp(self):
        load_alpha()

    def test_error(self):
        self.assertRaises(ValueError, alpha_hash, '* &$')
    def test_en(self):
        self.assertEqual(200011011, alpha_hash('$aBK!lz'))

    def test_uk(self):
        self.assertEqual(101001517, alpha_hash('$бАЛ?ня'))


if __name__ == '__main__':
    unittest.main()
