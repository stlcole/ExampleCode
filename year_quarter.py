import datetime
import warnings

from snippets import count_generator


#########################################################
#### Module and Class for working with date objects  ####
#### in the form YYYYQ; e.g. 20141 or `yq~ for short ####
#########################################################


yq_value = lambda yq: yq.yq if isinstance(yq, YearQtr) else yq
yq_object = lambda yq: yq if isinstance(yq, YearQtr) else YearQtr(yq)


def mon_year_to_yq(month, year):
    '''
    mon_year_to_yq takes month and year as arguments
    and returns standard yq form for the given arguments
    e.g.: month_year_to_yq(2014, 2) = 20141
    '''
    return (year * 10) + (month // 3) + 1


def today_yq():
    '''
    today_yq returns the the yq appropriate to today()
    '''
    today = datetime.date.today()
    return mon_year_to_yq(today.month, today.year)


def incr_yq(yq, n=1):
    '''
    incr_yq or `increment` yq returns the
    yq value after and n months to the initial value

    it accepts either an integer or YearQtr object
    as its first argument

    incr_qy defaults to adding 1 quarter
    '''
    yq = yq_value(yq)
    yq_year, yq_qtr = yq // 10, (yq % 10) - 1
    n_year, n_qtr = n // 4, n % 4

    qtrs = yq_qtr + n_qtr
    years = yq_year + n_year + qtrs // 4
    return years * 10 + qtrs % 4 + 1


def dif_yq(yq1, yq2):
    '''
    dif_yq returns the difference in quarters
    between the given yq1 values

    it accepts either yq values or yq objects

    when the count argument is
    '''

    yq1, yq2 = yq_object(yq1), yq_object(yq2)
    return (yq1.year - yq2.year) * 4 + (yq1.qtr - yq2.qtr)


def count_yq(start, stop=None, step=None):
    '''
    count_yq is a generator of sequential yq values

    given just a start value, the counter counts indefinitely

    given just a start value and a step value, the counter
    yields a value n steps if step > 0 or -n steps if step < 0

    if stop is < 1000, count_yq will count for
    n numbers of quarters, otherwise is will count from
    start to stop exclusive of the stop yq value

    (start, count > 0, step < 0) will count `count` down
    in increments of step, and counting down from start
    must always be given in this form, because of the
    following special case:

    # (start, count < 0) will count up to start, so
    # the stop value is the initial start value, and
    # the inferred start value is start-count
    '''


    # (20141, 3, -1) is not the equivalent of (20141, -3)
    # the former counts down and the later counts up

    assert YearQtr(yq_value(start))
    assert stop is None or isinstance(stop, int), "stop must be None or an int"
    assert step is None or isinstance(step, int), "stop must be None or an int"

    if not isinstance(step, type(None)):
        assert stop != 0, "Invalid step value of 0"

    count = stop if stop < 1000 else dif_yq(stop, start)  # May still be None

    # Special cases #
    # 1. if (start, count, step < 0), then the arguments to `count_generator`
    #    must be in the form

    count_generator_stop = None
    if stop is not None and stop > 0 and step is not None and step < 0:
        count = -count
        step = None

    if stop is not None and stop < 0 and step is None:
        count = stop + 1
        count_generator_stop = 1

    counting = count_generator(count, count_generator_stop, step)
    while counting:
        yield incr_yq(start, counting.next())


class YearQtr(object):
    '''
    YearQtr initializes with a yq value; i.e. YYYYQ, taking advantage
    of some limited testing of the given argument.
    
    self.yq = YYYYQ
    self.year is the YYYY part of the given yq value
    self.qtr is the Q part of the given yq value
      and if self.qtr is > 4, it converts the given yq value
      into its most appropriate form; e.g. 20147 => 20153
    
    incr(n) increments self.yq by n
    dif(yq) returns the difference in quarters between self.yq and yq
    count(yq, stop=None, step=None) provides a generator for yq values
      starting from self.yq
    '''

    def __init__(self, quarter_code):
        quarter_code = isinstance(quarter_code, long) and int(quarter_code) or quarter_code
        assert isinstance(quarter_code, int), \
            "YearQtr number must be an integer"
        assert quarter_code > 0, "YearQtr number must be greater than 0"

        self.yq = quarter_code
        self.year = self.yq // 10
        self.qtr = self.yq % 10

        if self.year < 2000:
            warnings.warn("Using a year earlier than 2000")

        if self.qtr > 4:
            warnings.warn("Using a quarter number greater than 4.")

        self.yq = self.incr(0)

    def incr(self, n):
        return incr_yq(self, n)

    def dif(self, yq):
        return dif_yq(self, yq)

    def count_yq(self, stop=None, step=None):
        return count_yq(self, stop, step)