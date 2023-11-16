"""
Bloom filter implementation
Source: https://www.geeksforgeeks.org/bloom-filters-introduction-and-python-implementation/
"""
import json
import math
from typing import Optional

import mmh3
from bitarray import bitarray


class BloomFilter:
    """
    Class for Bloom filter, using murmur3 hash function
    """

    def __init__(self,
        size: Optional[int] = None,
        num_hashes: Optional[int] = None,
        fp_prob: Optional[float] = None,
        items_count: Optional[float] = None,
    ):
        """
        size : int
            Size of bit array to use
        num_hashes : int
            Number of hash functions to use
        items_count : int
            Number of items expected to be stored in bloom filter
        fp_prob : float
            False Positive probability in decimal

        - You can declare size manually or pass items_count and fp_prob to calculate it
        - You can declare num_hashes manually or pass size and items_count to calculate it
            (size can be calculated from items_count and fp_prob)
        """

        if size is None:
            assert items_count is not None and fp_prob is not None, \
                "You must specify either size or items_count and fp_prob"

        if num_hashes is None:
            assert items_count is not None, \
                "You must specify either num_hashes, or size and items_count or items_count and fp_prob"

        # Size of bit array to use
        self.size = size if size is not None else self.get_size(items_count, fp_prob)

        # number of hash functions to use
        self.hash_count = num_hashes if num_hashes is not None else self.get_hash_count(self.size, items_count)

        # Bit array of given size
        self.bit_array = bitarray(self.size)

        # initialize all bits as 0
        self.bit_array.setall(0)

        self.items_stored = 0

    def __str__(self):
        data = {
            "size": self.size,
            "hash_count": self.hash_count,
            "fp_prob": f'{self.fp_prob:.5f}',
            "items_stored": self.items_stored,
        }
        return f"BloomFilter({data})"

    @property
    def fp_prob(self):
        """Returns the false positive probability of the filter according to the number of items stored"""
        return (1.0 - ((1.0 - 1.0 / self.size) ** (self.hash_count * self.items_stored))) ** self.hash_count

    def add(self, item):
        """
        Add an item in the filter
        """
        self.items_stored += 1
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
        # Increase n by 1, to garantee false positive rate is lower than p
        n += 1
        m = -(n * math.log(p))/(math.log(2)**2)
        return math.ceil(m)

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

    def save(self, path):
        """
        Save the bloom filter to a file
        """
        with open(path, "w") as f:
            serialized = {
                "size": self.size,
                "num_hashes": self.hash_count,
                "bit_array": self.bit_array.tobytes().hex(),
                "items_stored": self.items_stored,
            }
            json.dump(serialized, f, indent=4)

    @classmethod
    def load(cls, path):
        """
        Load a bloom filter from a file
        """
        with open(path, "r") as f:
            serialized = json.load(f)
            bf = cls(size=serialized["size"], num_hashes=serialized["num_hashes"])
            bf.bit_array = bitarray()
            bf.bit_array.frombytes(bytes.fromhex(serialized["bit_array"]))
            bf.bit_array = bf.bit_array[:bf.size]
            bf.items_stored = serialized["items_stored"]
            return bf
