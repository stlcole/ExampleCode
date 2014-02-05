__author__ = 'cole'

import unittest

class TestGeneratorLength(unittest.TestCase):
    def test_generator_length(self):
        from snippets import generator_length, prime_generator

        primes = prime_generator(count=99)
        self.assertEqual(generator_length(primes), 99)


class TestIsPrime(unittest.TestCase):
    def test_is_prime(self):
        from snippets import is_prime

        test_list = [is_prime(n) for n in xrange(12)]
        self.assertEqual(
            test_list,
            [False, False, True, True, False, True, False, True, False, False, False, True]
        )


class TestNumberOfDivisors(unittest.TestCase):
    def test_number_of_divisors(self):
        from snippets import divisors_of_n

        n = 4 * 9 * 25
        self.assertEqual(
            divisors_of_n(n),
            [1, 2, 3, 4, 5, 6, 9, 10, 12, 15, 18, 20, 25, 30, 36, 45, 50, 60, 75, 90, 100, 150, 180, 225, 300, 450, 900]
        )


class TestDivisorsOfN(unittest.TestCase):
    def test_divisors_of_n(self):
        assert True

    def test_divisors_of_n_less_than(self):
        from snippets import divisors_of_n, divisors_for_n_less_than

        divisor_lists = divisors_for_n_less_than(100)

        for i, d_list in enumerate(divisor_lists):
            self.assertEqual(set(d_list), set(divisors_of_n(i+1)))
