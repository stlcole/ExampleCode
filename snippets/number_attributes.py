__author__ = 'cole'

import itertools
from operator import mul


def generator_length(iter):
    try:
        return len(iter)
    except:
        return sum(1 for _ in iter)


def is_prime(n):
    is_divisible = lambda n, p: not(n % p)

    if n <= 1:
        return False

    if n < 4:
        return True

    if is_divisible(n, 2):
        return False

    if n < 9:
        return True

    if any([
        is_divisible(n, 3),
        is_divisible(n, 5),
        is_divisible(n, 7),
    ]):
        return False

    floor = (n ** 0.5) // 1
    f = 5
    while f <= floor:
        if not n % f or not n % (f + 2):
            return False

        f += 6

    return True


def divisors_of_n(n):
    from .number_generators import prime_factors_and_powers_for_n_generator

    ##  WORKFLOW ##
    #  1. get the (factor, power) for each factor in n
    #  2. create a list of divisors for each prime, e.g. [[1, 2, 4, 8], [1, 3, 9, 27], [1, 5, 25, 125]]
    #  3. generate all possible combinations of prime divisors,
    #    e.g. [[1,1,1], [2,1,1], [1,3,1], [1,1,5], [2,3,1], ..., [8,27,125]]
    #  4. the divisors of n are list of products of each combination of prime divisors

    factors_and_powers = prime_factors_and_powers_for_n_generator(n)
    prime_divisors = [[f ** x for x in xrange(0, p + 1)] for f, p in factors_and_powers]

    combinations_of_prime_divisors = itertools.product(*prime_divisors)  # Step 3
    divisor_generator = (reduce(mul, combination, 1) for combination in combinations_of_prime_divisors)  # Step 4
    return sorted(list(divisor_generator))


def divisors_for_n_less_than(less_than):
    '''
    divisors_for_n_less_than(less_than) returns a list of lists. The divisor list for number n
    is the n-1 index in the list of lists. The return starts [[1], [1,2], [1,3], [1,2,4], ...]
    '''

    ## ALGORITHM WORKFLOW
    # 1. assemble a list of lists of [1] where list length is (less_than - 1) (which handles divisor = 1)
    # 2. start with divisor = 2, and for every 2nd list append 2 (the 0th list is for n = 1, etc.)
    # 3. count up the divisors until divisor = less_than, e.g. if less_than = 100 and divisor = 99,
    #    the algorithm give an end condition where xrange(98, 99, 99) = 98,
    #    which is the 99th list i.e. divisor_lists[98], and appends 99 (divisor = 99)

    divisor_lists = [[1] for _ in xrange(less_than-1)]
    divisor = 2

    while divisor < less_than:
        for i in xrange(divisor-1, less_than-1, divisor):
            divisor_lists[i].append(divisor)
        divisor += 1

    return divisor_lists