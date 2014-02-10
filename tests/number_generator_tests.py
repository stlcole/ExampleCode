__author__ = 'cole'

import itertools
import unittest


class TestGenerators(unittest.TestCase):
    def test_generator_limiter(self):
        from snippets import generator_limiter
        from snippets.number_generators import _fibonacci_generator


        gen = generator_limiter(filter_by=(lambda x: x & 1))
        self.assertEqual(gen.next(), 1)
        self.assertEqual(gen.next(), 3)
        self.assertEqual(gen.next(), 5)

        gl = generator_limiter(count=20)
        self.assertEqual(list(gl), range(20))

        gl = generator_limiter(count=20, last_only=True)
        self.assertEqual(list(gl), [19])

        gl = generator_limiter(limit=21, as_tuple=2)
        self.assertEqual(
            list(gl),
            [(0, 1), (2, 3), (4, 5), (6, 7), (8, 9), (10, 11), (12, 13), (14, 15), (16, 17), (18, 19)]
        )

        gl = generator_limiter(limit=21, last_only=True, as_tuple=2)
        self.assertEqual(list(gl), [(18, 19)])

        gl = generator_limiter(limit=21, count=4, as_tuple=2)
        self.assertEqual(list(gl), [(0, 1), (2, 3), (4, 5), (6, 7)])

        gl = generator_limiter(limit=21, count=4, last_only=True, as_tuple=2)
        self.assertEqual(list(gl), [(6, 7)])

        gen = _fibonacci_generator()
        gl = generator_limiter(gen, limit=100, as_tuple=3)
        self.assertEqual(list(gl), [(1, 1, 2), (3, 5, 8), (13, 21, 34)])

        gen = _fibonacci_generator()
        gl = generator_limiter(gen, limit=100, last_only=True, as_tuple=3)
        self.assertEqual(list(gl), [(13, 21, 34)])

    def test_counter(self):
        from snippets import count_generator

        self.assertEqual(list(count_generator(10)), [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.assertEqual(list(count_generator(10, -2)), [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, -1])
        self.assertEqual(list(count_generator(1, 9, 2)), [1, 3, 5, 7])
        self.assertEqual(list(count_generator(9, -2, -2)), [9, 7, 5, 3, 1, -1])

        count = count_generator()
        self.assertEqual(count.next(), 0)
        self.assertEqual(count.next(), 1)
        self.assertEqual(count.next(), 2)
        self.assertEqual(count.next(), 3)

    def test_fibonacci_generator(self):
        from snippets import fibonacci_generator
        fib_numbers = fibonacci_generator()

        self.assertEqual(fib_numbers.next(), 1)
        self.assertEqual(fib_numbers.next(), 1)
        self.assertEqual(fib_numbers.next(), 2)
        self.assertEqual(fib_numbers.next(), 3)
        self.assertEqual(fib_numbers.next(), 5)
        self.assertEqual(fib_numbers.next(), 8)

        # test as_tuple=True
        fib_numbers = fibonacci_generator(as_tuple=True)
        self.assertEqual(fib_numbers.next(), (1, 1, 2))
        self.assertEqual(fib_numbers.next(), (3, 5, 8))
        self.assertEqual(fib_numbers.next(), (13, 21, 34))

        # test generator using a number less than lambda
        fib_numbers = fibonacci_generator(limit=(lambda x: x < 22))
        self.assertEqual(list(fib_numbers), [1, 1, 2, 3, 5, 8, 13, 21])

        fib_fails_at_a = fibonacci_generator(limit=(lambda x: x < 1))
        try:
            list(fib_fails_at_a)
            assert False

        except AssertionError:
            pass

        fib_fails_at_c = fibonacci_generator(limit=(lambda x: x < 2))
        self.assertEqual(list(fib_fails_at_c), [1, 1])

        # test generator using a number of digits less than lambda
        fib_numbers = fibonacci_generator(limit=(lambda x: len(str(x)) < 3))
        self.assertEqual(list(fib_numbers), [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89])

        # test generator using both as_tuple and limit
        fib_numbers = fibonacci_generator(as_tuple=True, limit=(lambda x: x < 55))
        self.assertEqual(list(fib_numbers), [(1, 1, 2), (3, 5, 8), (13, 21, 34)])

    def test_simple_fibonacci_generator(self):
        from snippets.number_generators import _fibonacci_generator, fibonacci_generator

        fibs = _fibonacci_generator()
        old_fibs = fibonacci_generator()

        for _ in xrange(20):
            self.assertEqual(fibs.next(), old_fibs.next())

    def test_private_prime_generator(self):
        from snippets.number_generators import _prime_generator

        primes = _prime_generator()
        self.assertEqual(primes.next(), 2)
        self.assertEqual(primes.next(), 3)
        self.assertEqual(primes.next(), 5)
        self.assertEqual(primes.next(), 7)
        self.assertEqual(primes.next(), 11)
        self.assertEqual(primes.next(), 13)
        self.assertEqual(primes.next(), 17)
        self.assertEqual(primes.next(), 19)
        self.assertEqual(primes.next(), 23)
        self.assertEqual(primes.next(), 29)
        self.assertEqual(primes.next(), 31)
        self.assertEqual(primes.next(), 37)

    def test_prime_generator(self):
        from snippets import prime_generator

        primes = prime_generator()

        self.assertEqual(primes.next(), 2)
        self.assertEqual(primes.next(), 3)
        self.assertEqual(primes.next(), 5)
        self.assertEqual(primes.next(), 7)
        self.assertEqual(primes.next(), 11)
        self.assertEqual(primes.next(), 13)
        self.assertEqual(primes.next(), 17)
        self.assertEqual(primes.next(), 19)
        self.assertEqual(primes.next(), 23)

        primes = prime_generator(count=12)
        self.assertEqual(list(primes), [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37])

        primes = prime_generator(limit=60)
        self.assertEqual(list(primes), [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59])

    def test_prime_factor_generator(self):
        from snippets import prime_factor_generator
        prime_factors = prime_factor_generator(232792560)

        self.assertEqual(prime_factors.next(), 2)
        self.assertEqual(prime_factors.next(), 3)
        self.assertEqual(prime_factors.next(), 5)
        self.assertEqual(prime_factors.next(), 7)
        self.assertEqual(prime_factors.next(), 11)
        self.assertEqual(prime_factors.next(), 13)
        self.assertEqual(prime_factors.next(), 17)
        self.assertEqual(prime_factors.next(), 19)

        prime_factors = prime_factor_generator(232792560)
        self.assertEqual(list(prime_factors), [2, 3, 5, 7, 11, 13, 17, 19])

    def test_prime_factors_and_powers_for_n_generator(self):
        from snippets import prime_factors_and_powers_for_n_generator

        factors_and_powers = prime_factors_and_powers_for_n_generator(2**3 * 3**4 * 5**7)

        self.assertEqual(list(factors_and_powers), [(2, 3), (3, 4), (5, 7)])

    def test_private_primes_from_quadratic(self):
        from snippets.number_generators import _primes_from_quadratic

        p_list = list(_primes_from_quadratic())
        # print len(set([p for _, p in p_list]))
        # for p in p_list:
        #     print(p)

    def test_palindromic_number_generator(self):
        from snippets import palindromic_number_generator

        palindromes = palindromic_number_generator()
        self.assertEqual(palindromes.next(), 11)
        self.assertEqual(palindromes.next(), 22)
        self.assertEqual(palindromes.next(), 33)
        self.assertEqual(palindromes.next(), 44)
        self.assertEqual(palindromes.next(), 55)
        self.assertEqual(palindromes.next(), 66)
        self.assertEqual(palindromes.next(), 77)
        self.assertEqual(palindromes.next(), 88)
        self.assertEqual(palindromes.next(), 99)
        self.assertEqual(palindromes.next(), 1001)
        self.assertEqual(palindromes.next(), 1111)
        self.assertEqual(palindromes.next(), 1221)

        palindromes = palindromic_number_generator(999, 0)
        self.assertEqual(palindromes.next(), 999999)

    def test_triplet_generator(self):
        from snippets import bound_triplet_generator

        triplets = bound_triplet_generator(6)
        self.assertEqual(list(triplets), [(1, 1, 4), (1, 2, 3), (1, 3, 2), (2, 1, 3), (2, 2, 2), (3, 1, 2)])

    def test_triangle_number_generator(self):
        from snippets import triangle_number_generator

        triangle_numbers = triangle_number_generator()

        self.assertEqual(triangle_numbers.next(), 1)
        self.assertEqual(triangle_numbers.next(), 3)
        self.assertEqual(triangle_numbers.next(), 6)

    def test_collatz_generator(self):
        from snippets import collatz_generator

        collatz_sequence = collatz_generator(13)

        self.assertEqual(list(collatz_sequence), [40, 20, 10, 5, 16, 8, 4, 2, 1])

    def test_muliples_of_n_less_than(self):
        from snippets import multiples_of_n_less_than

        multiples_of_n = multiples_of_n_less_than(3, 100)

        self.assertEqual(multiples_of_n.next(), 3)
        self.assertEqual(multiples_of_n.next(), 9)

        multiples_of_n = multiples_of_n_less_than(3, 200)

        self.assertEqual(list(multiples_of_n), [3, 9, 27, 81])