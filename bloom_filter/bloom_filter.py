"""
Bloom filter implementation
Source: https://www.geeksforgeeks.org/bloom-filters-introduction-and-python-implementation/
"""
import math

import mmh3
from bitarray import bitarray


class BloomFilter:
    """
    Class for Bloom filter, using murmur3 hash function
    """

    def __init__(self, items_count, fp_prob):
        """
        items_count : int
            Number of items expected to be stored in bloom filter
        fp_prob : float
            False Positive probability in decimal
        """
        # False possible probability in decimal
        self.fp_prob = fp_prob

        # Size of bit array to use
        self.size = self.get_size(items_count, fp_prob)

        # number of hash functions to use
        self.hash_count = self.get_hash_count(self.size, items_count)

        # Bit array of given size
        self.bit_array = bitarray(self.size)

        # initialize all bits as 0
        self.bit_array.setall(0)

    def __str__(self):
        return f"BloomFilter(size={self.size}, hash_count={self.hash_count}, fp_prob={self.fp_prob})"

    def add(self, item):
        """
        Add an item in the filter
        """
        digests = []
        for i in range(self.hash_count):

            # create digest for given item.
            # i work as seed to mmh3.hash() function
            # With different seed, digest created is different
            digest = mmh3.hash(item, i) % self.size
            digests.append(digest)

            # set the bit True in bit_array
            self.bit_array[digest] = True

    def check(self, item):
        """
        Check for existence of an item in filter
        """
        for i in range(self.hash_count):
            digest = mmh3.hash(item, i) % self.size
            if self.bit_array[digest] == False:

                # if any of bit is False then,its not present
                # in filter
                # else there is probability that it exist
                return False
        return True

    @classmethod
    def get_size(self, n, p):
        """
        Return the size of bit array(m) to used using
        following formula
        m = -(n * lg(p)) / (lg(2)^2)
        n : int
            number of items expected to be stored in filter
        p : float
            False Positive probability in decimal
        """
        m = -(n * math.log(p))/(math.log(2)**2)
        return int(m)

    @classmethod
    def get_hash_count(self, m, n):
        """
        Return the hash function(k) to be used using
        following formula
        k = (m/n) * lg(2)

        m : int
            size of bit array
        n : int
            number of items expected to be stored in filter
        """
        k = (m/n) * math.log(2)
        return int(k)

    @classmethod
    def load(cls, path):
        """
        Load a bloom filter from a file
        """
        with open(path, 'rb') as f:
            return cls._from_bytes(cls, f.read())

    def save(self, path):
        """
        Save a bloom filter to a file
        """
        with open(path, 'wb') as f:
            f.write(self._to_bytes())

    def _to_bytes(self):
        """
        Convert the bloom filter to bytes
        """
        return self.bit_array.tobytes()

    def _from_bytes(self, data):
        """
        Load a bloom filter from bytes
        """
        self.bit_array = bitarray()
        self.bit_array.frombytes(data)
        self.size = len(self.bit_array)
        self.hash_count = self.get_hash_count(self.size, 1)
        return self
