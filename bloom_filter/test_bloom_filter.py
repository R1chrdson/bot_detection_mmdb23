import unittest
from bloom_filter.bloom_filter import BloomFilter

class TestBloomFilter(unittest.TestCase):
    def test_add_and_check(self):
        bf = BloomFilter(10, 0.1)
        bf.add('Hello')
        self.assertTrue(bf.check('Hello'))
        self.assertFalse(bf.check('Hello1'))

    def test_save_and_load(self):
        bf = BloomFilter(10, 0.1)
        bf.add('Hello')
        bf.save('data/test.bf')
        bf.load('data/test.bf')
        self.assertFalse(bf.check('Hello1'))
        self.assertTrue(bf.check('Hello'))

    def test_check_nonexistent_element(self):
        bf = BloomFilter(10, 0.1)
        bf.add('Hello')
        self.assertFalse(bf.check('Hello1'))

    def test_check_existing_element(self):
        bf = BloomFilter(10, 0.1)
        bf.add('Hello')
        self.assertTrue(bf.check('Hello'))


if __name__ == '__main__':
    unittest.main()
