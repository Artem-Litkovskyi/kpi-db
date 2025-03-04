import unittest
from alpha_hash import *


class MyTestCase(unittest.TestCase):
    def setUp(self):
        load_alpha()

    def test_error(self):
        self.assertRaises(ValueError, alpha_hash, '* &$')
    def test_en(self):
        self.assertEqual(20055900000, alpha_hash('$aBK!lz'))

    def test_uk(self):
        self.assertEqual(10055900000, alpha_hash('$бАЛ?ня'))

    def test_long(self):
        self.assertEqual(21111111111, alpha_hash('c' * STRING_LENGTH * 2))


if __name__ == '__main__':
    unittest.main()
