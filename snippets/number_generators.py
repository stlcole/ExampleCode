__author__ = 'cole'

from collections import Iterable
import itertools
import warnings

from .number_attributes import is_prime


def generator_limiter(generator=None, limit=None, count=None, filter_by=None, last_only=False, as_tuple=0):
    '''
    generator_limiter(generator, limit, count, filter_by, last_only, as_tuple)
    will operate the given generator within the conditions established by limit,
    count, last_only, and as_tuple.

        generator: provides a generator function to be subject to the associated
        limits as detailed by limit, count, last_only and as_tuple. It defaults to
        itertools.count if no generator is provided.

        limit: stops the generator if the next yield value is not less than the limit

        count: limits the number of yielded results to count

        filter_by: provides a function (usual a lambda) which provide condition testing
        for each generated result.

        last_only: yields only the last value for a given generator if last_only
        is set to True. Combine with count for infinite generators.

        as_tuple: yields results as a tuple of value set by as_tuple=x.
    '''

    if count:
        assert isinstance(count, int or float) and count > 0, \
            'count must be a positive numeric value'

        if isinstance(count, float):
            warnings.warn('count is a float value and will be truncated to nearest int')
            count = int(count)

    is_within_limit = limit and (lambda x: x < limit) or (lambda x: True)
    generator = generator or itertools.count()

    if filter_by:
        generator = itertools.ifilter(filter_by, generator)

    gen_instance = enumerate(generator)
    index, value = gen_instance.next()
    last_value, tuple_values, last_tuple, yielded = value, tuple(), tuple(), 0

    while is_within_limit(value):
        if as_tuple:
            tuple_values += (value,)
            if len(tuple_values) == as_tuple:
                last_tuple, tuple_values = tuple_values, tuple()

            else:
                index, value = gen_instance.next()
                continue

        if not last_only:
            yield as_tuple and last_tuple or value

        last_value, (index, value) = value, gen_instance.next()

        if count > 0:
            counted = as_tuple and index // as_tuple or index
            if counted == count:
                break

    if last_only:
        if as_tuple:
            yield last_tuple

        else:
            yield last_value


def count_generator(*args):
    '''
    count_generator() is designed to be counting iterator which allows for
    a more intuitive use of arguments, inferring appropriate
    start, stop and step values. It obviates the need to switch between
    iter(xrange()) and itertools.count() depending on use-case.

    using no arguments:
      count_generator() counts up from 0. "Count forever"

    using 1 argument: "Count to X". e.g.:
      count_generator(3) counts up to 3 exclusive; i.e 0, 1, 2

    using 2 arguments: "Count from X to Y". e.g.:
      count_generator(7, 3) counts from 7 to 3 exclusive; i.e. 7, 6, 5, 4

    special 2 argument case with None as the 2nd argument: "Count from X forever".
      e.g.: count_generator(7, None) counts up from 7.

    using 3 arguments: "Count from X to Y in steps of Z". e.g.:
     count_generator(3, -4, -2) counts down in steps of two; i.e. 3, 1, -1, -3

    special 3 argument case, with None as the 2nd argument: "Count from X in steps of Z".
    e.g.: count_generator(3, None, -2) counts 3, 1, -1 ..
      this case is an extension of the 2 argument case using None as the 2nd argument
    '''

    assert len(args) < 4, 'Uses only start, stop, step values'

    args = list(args)
    while args and args[-1] is None:
        args.pop()

    if len(args) == 3:
        start, stop, step = args
        if start is None and stop is None:
            assert step != 0, "Invalid arguments (None, None, 0)"

            _gen = itertools.count() if abs(step) == 1 \
                else itertools.ifilter(lambda x: x % abs(step) == 0, itertools.count())

            return step > 0 and _gen or itertools.imap(lambda x: x * -1, _gen)

        if stop is not None:
            assert not(start > stop and step > 0), 'cannot use a positive step when counting from high to low'
            assert not(start < stop and step < 0), 'cannot use a negative step when counting from low to high'

            return iter(xrange(start, stop, step))

        else:
            return itertools.count(start, step)

    if len(args) == 2:
        start, stop = args

        if stop is not None:
            step = 1 if stop > start else -1
            return iter(xrange(start, stop, step))

        else:
            return itertools.count(start)

    start = args and args[0]
    if not start:
        return itertools.count()

    return iter(xrange(start)) if start > 0 else itertools.imap(lambda x: -x, xrange(abs(start)))


def _fibonacci_generator():
    a = b = 1
    yield a
    a, b = b, a + b
    while True:
        yield a
        a, b = b, a + b


def fibonacci_generator(as_tuple=False, limit=None, last_only=False):
    '''
    fibonacci_generator(as_tuple=False, limit=None) yields the classic sequence of fibonacci numbers.
        as_tuple=True will cause the generator to yield tuples of numbers,
            e.g. [1, 1, 2], [3, 5, 8], etc.

        limit=(lambda x: some truth test) e.g. limit=(lambda x: x < 1000)

        when using both as as_tuple and limit, the a tuple is returned only if all
        tuple numbers are less than the limit
    '''

    if as_tuple or limit or last_only:
        as_tuple = as_tuple and 3 or 0
        return generator_limiter(_fibonacci_generator(), limit=limit, last_only=last_only, as_tuple=as_tuple)

    else:
        return _fibonacci_generator()


def _primes_from_quadratic():
    counter = itertools.count()
    p = 2
    while is_prime(p):
        n = counter.next()
        p = n ** 2 + n * -61 + 971

        yield n, p


def _prime_generator():
    '''
    _prime_generator yields successive prime numbers
    '''

    # http://stackoverflow.com/questions/2211990/how-to-implement-an-efficient-infinite-generator-of-prime-numbers-in-python/3796442#3796442

    D = {9: 3, 25: 5}
    yield 2
    yield 3
    yield 5
    MASK = 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0,
    MODULOS = frozenset((1, 7, 11, 13, 17, 19, 23, 29))

    for q in itertools.compress(
            itertools.islice(itertools.count(7), 0, None, 2),
            itertools.cycle(MASK)):

        p = D.pop(q, None)  # first added p is p = 49

        if p is None:
            D[q*q] = q  # when q = 7, D[49] = 7
            yield q

        else:  # e.g. q = 49, p = 7
            x = q + 2 * p  # 51 * 7 = 357

            while x in D or (x % 30) not in MODULOS:
            #  x % 30 = 27, in MODULOS would suggest something like 31, 37, 41, 43, 47, 49, 53, 59
                x += 2 * p
                #  x += 2 * 7, x = 357 + 14 = 371, 371 % 30 = 11, 385 % 30 = 25

            D[x] = p

            #  D[385] = 7 which is in MODULOS, so this simply flags 385 as not prime
            #  so when q = 385, it gets popped from D, and is tested
            #  q=385: x = 385 + 14 = 399 then 413, 413 % 30 = 23, and 413 into D


def prime_generator(count=None, limit=None, last_only=False):
    '''
    prime_generator(count=None, limit=None) yields successive prime numbers
        count=n will limit the number of primes to n
        limit=n will strop yielding primes once the next prime will exceed limit=n
    '''

    if count or limit or last_only:
        limit_value = limit and limit or 0
        limit = limit and (lambda x: x < limit_value) or None

        return generator_limiter(_prime_generator(), limit=limit, count=count, last_only=last_only)

    else:
        return _prime_generator()


#### COLE'S OLD PRIME GENERATOR, LEFT HERE FOR SHOW ####
# def prime_generator(count=None):
#     '''
#     prime_generator yields primes, with a count limit specified by the first argument, if any
#     '''
#
#     number_and_prime_test = lambda number: (number, is_prime(number))
#     is_within_limit = count and (lambda count: count > 0) or (lambda count: True)
#
#     for prime in (2, 3, 5, 7):
#         yield prime
#
#     is_prime_generator = itertools.imap(number_and_prime_test, itertools.count(11, 6))
#     count = count and count - 4 or False
#
#     while is_within_limit(count):
#         number, is_prime_number = next(is_prime_generator)
#         if is_prime_number:
#             yield number
#             count = count and count - 1
#
#         if is_prime(number + 2):
#             # count is either False or an int, and if it either False or greater than 0, then yield
#             if any([
#                 isinstance(count, int) and count > 0,
#                 isinstance(count, bool),
#             ]):
#                 yield number + 2
#             count = count and count - 1


def prime_factor_generator(number):
    primes = prime_generator()
    prime = primes.next()

    while prime <= number:
        if number % prime == 0:
            yield prime

        while number % prime == 0:
            number /= prime

        prime = primes.next()


def prime_divisor_generator(limit, prime_factors=None):
    prime_factors = prime_factors or prime_generator(limit//2)

    for prime_factor in prime_factors:
        n = prime_factor
        while n < limit:
            yield n
            n *= prime_factor


def prime_factors_and_powers_for_n_generator(n):
    prime_factors = prime_factor_generator(n)

    for prime_factor in prime_factors:
        power, number = 0, n
        while number % prime_factor == 0:
            power += 1
            number /= prime_factor

        yield prime_factor, power


def palindromic_number_generator(*args):
    '''
    palindromic_number_generator yields palindromes from a range of numbers
    the sequence begins 11, 22, .. 1001, 1111, 1221,  ..

    0 is not considered a palindromic number
    '''

    numbers = count_generator(*args)

    while True:
        number = numbers.next()
        if number == 0:
            continue
        yield int(str(number) + str(number)[::-1])


def bound_triplet_generator(triplet_total):
    '''
    bound_triplet_generator(triplet_total) returns all triplets of ints which sum to the triplet_total
    '''
    for a in xrange(1, triplet_total - 2):
        for b in xrange(1, triplet_total - a - 1):
            yield a, b, triplet_total - a - b


def triangle_number_generator():
    numbers = itertools.count()
    triangle_number = numbers.next()
    while True:
        triangle_number += numbers.next()
        yield triangle_number


def collatz_generator(n):
    '''
    collatz_generator(n) yields a sequence of numbers according to two rules:
        a) if n is even, n = n / 2
        b) if n is odd, n = 3n + 1
    a collatz sequence stops when n equals 1
    '''
    while n != 1:
        n = n & 1 and (3 * n + 1) or n / 2
        yield n


def multiples_of_n_less_than(n, less_than):
    m = n
    while m < less_than:
        yield m
        m *= n