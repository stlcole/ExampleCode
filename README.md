This repository contains examples of my code and their associated tests. The purpose is to demonstrate a variety of contexts and coding challenges.

`year_quarter` or `yq` for short, provides methods and a class for date values in the form YYYYQ, a date form which is often used for modeling the financial performance of companies. The basic methods are a form of adding, differencing, and sequence generation. The `YearQuarter` class initialize on a given YYYYQ value, and provides the given methods against the initialized values.

`snippets.models.LambdaCode` provides a django model for lambda construction and implementation, helpful when performance measurements against a specific event can be arbitrary. For example, one period's incentive comp plan might be different than another period's incentive comp plan. `LambdaCode` objects can be linked to period objects for the efficient management of these relationships, and provide the means to return the appropriate performance metrics based on a given period's data.

`custom_user` is a Django app which provides an email-based User model (called Participant herein). `custom_user` contains the necessary model, model manager, forms, and views to create a custom_user and authentic a user's login.

`snippets.number_generators` contains several generators (e.g., `count_generator`, `fibonacci_generator`, `prime_generator`, etc.), many of which are used to solve [ProjectEuler][PE] problems. After building several of these generators, I built `snippets.number_generators.generator_limiter` which handles many of the typical conditions which might be associated with implementing a generator, such as limit the generated numbers to some arbitrary condition (e.g. `limit = lambda x: x & 1`, which would yield only odd numbers), limit the generator to an arbitrary count (yield 10 values then stop), provide generated numbers in tuples of arbitrary length, or yield only the nth value. As a matter of style, I often use a generator provide a consideration set, then run the generator against some condition to provide a set of appropriate values.


 [PE]: http://projecteuler.net