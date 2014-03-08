__author__ = 'cole'

import datetime
import warnings

from snippets import snippet as snp


######################################################################
#### Module, Class, and Mixin for working with date objects       ####
#### in the form YYYYQ; e.g. 20141 or `yq_quarter_code~ for short ####
######################################################################


yq_value = lambda yq: yq.yq if isinstance(yq, YearQtr) else yq
yq_object = lambda yq: yq if isinstance(yq, YearQtr) else YearQtr(yq)

def mon_year_to_yq(month, year):
    '''
    mon_year_to_yq takes month and year as arguments
    and returns standard yq_quarter_code form for the given arguments
    e.g.: month_year_to_yq(2014, 2) = 20141
    '''
    return (year * 10) + (month // 3) + 1


def today_yq():
    '''
    today_yq returns the the yq_quarter_code appropriate to today()
    '''
    today = datetime.date.today()
    return mon_year_to_yq(today.month, today.year)


def incr_yq(yq, n=1, m=1):
    '''
    incr_yq or `increment` yq_quarter_code returns the
    yq_quarter_code value after and n months to the initial value

    it accepts either an integer or YearQtr object
    as its first argument

    incr_qy defaults to adding 1 quarter
    '''

    assert m in {1, -1}, "Give a -1 second argument for subtraction"
    n *= m

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

    it accepts either yq_quarter_code values or yq_quarter_code objects

    when the count argument is
    '''

    yq1, yq2 = yq_object(yq1), yq_object(yq2)
    return (yq1.year - yq2.year) * 4 + (yq1.qtr - yq2.qtr)


def count_yq(start, stop=None, step=None, include=True):
    '''
    count_yq is a generator of sequential yq_quarter_code values

    given just a start value, the counter counts indefinitely

    given just a start value and a step value, the counter
    yields a value n steps if step > 0 or -n steps if step < 0

    if stop is < 1000, count_yq will count for
    n numbers of quarters, otherwise is will count from
    start to stop exclusive of the stop yq_quarter_code value

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
    stop = isinstance(stop, long) and int(stop) or stop

    assert stop is None or isinstance(stop, int), "stop must be None or an int"
    assert step is None or isinstance(step, int), "stop must be None or an int"

    if not isinstance(step, type(None)):
        assert stop != 0, "Invalid step value of 0"

    count = stop if stop < 1000 else dif_yq(stop, start)  # May still be None
    if count is not None:
        count += -1 if stop > 999 and not include else 0  # if stop=YYYYQ and include=False

    # Special cases #
    # 1. if (start, count, step < 0), then the arguments to `count_generator`
    #    must be in the form
    # 2. if (start, count, step=1) will create args of (count, None, 1)
    #    which will count indefinitely, starting at count, so must be
    #    passed to count_generator in the form (count, None, None)

    stop_from_count = None
    if stop is not None and stop > 0 and step is not None and step < 0:
        count = -count
        step = None

    if stop is not None and stop < 0 and step is None:
        count = stop + 1
        stop_from_count = 1

    if stop_from_count is None and step == 1:
        step = None

    directions = [count or stop, stop_from_count, step]
    direction = reduce(lambda x, y: x * y, [snp.one_zero_minus_one(d) for d in directions if d is not None])

    change_start = 1 * (not include) * direction
    start = incr_yq(start, change_start)

    counting = snp.count_generator(count, stop_from_count, step)
    while counting:
        yield incr_yq(start, counting.next())


class YearQtr(object):
    '''
    YearQtr initializes with a yq_quarter_code value; i.e. YYYYQ, taking advantage
    of some limited testing of the given argument.

    self.yq_quarter_code = YYYYQ
    self.year is the YYYY part of the given yq_quarter_code value
    self.qtr is the Q part of the given yq_quarter_code value
      and if self.qtr is > 4, it converts the given yq_quarter_code value
      into its most appropriate form; e.g. 20147 => 20153

    incr(n) increments self.yq_quarter_code by n
    dif(yq_quarter_code) returns the difference in quarters between self.yq_quarter_code and yq_quarter_code
    count(yq_quarter_code, stop=None, step=None) provides a generator for yq_quarter_code values
      starting from self.yq_quarter_code
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

        self.yq = self.incr(0)

    def incr(self, n, m=1):
        return incr_yq(self, n, m)

    def dif(self, yq):
        return dif_yq(self, yq)

    def count_yq(self, stop=None, step=None, include=True):
        return count_yq(self, stop, step, include)

    def prior_quarter_code(self):
        return self.incr(-1)

    def next_quarter_code(self):
        return self.incr(1)

    def n_quarters_ago(self, n, include=False):
        n -= 1 * include if n != 0 else 0
        return self.incr(-n)

    def past_n_quarters(self, n):
        return self.count_yq(self.n_quarters_ago(n), include=True)

    def prior_n_quarters(self, n):
        return self.count_yq(self.n_quarters_ago(n - 1), include=False)

    def quarter_codes(self, n, include_n=True):
        if n == 0 or self.yq == n:
            return include_n and iter([self.yq]) or None

        if n < 1000:
            n = (n + 1 * include_n)
        else:
            n = -self.dif(n)  # if self.yc > n, we want to count down & n is neg
            n += 1 * snp.one_zero_minus_one(n) if include_n else 0

        return self.count_yq(n)


class TimeFrameMixin(object):
    _start_code = None
    _end_code = None
    _current_quarter_code = None

    def set_current_quarter_code(self, quarter_code):
        assert quarter_code >= self._start_code and quarter_code <= self.end_code, \
            "Current Quarter must be within time frame"
        self._current_quarter_code = YearQtr(quarter_code).yq

    @property
    def current_quarter_code(self):
        if self._current_quarter_code is None:
            self._current_quarter_code = self.end_code
        return self._current_quarter_code

    @property
    def yq_current(self):
        return YearQtr(self.current_quarter_code)

    @property
    def prior_quarter_code(self):
        return self.yq_current.prior_quarter_code()

    @property
    def next_quarter_code(self):
        return self.yq_current.next_quarter_code()

    def set_time_frame(self, start_code=None, n=None, current_quarter=None, inclusive=True):
        #### SET_TIME_FRAME ####
        # set_time_frame either sets the time frame given
        # explicit arguments or tests self for the appropriate
        # quarter code or returns the default

        assert start_code > 999, "Requires start_code"

        if start_code is not None:
            start_code = YearQtr(start_code)
            if n is None or n == 0:  # No time frame
                assert inclusive, "Cannot exclude the only quarter from a 1 quarter analysis. Set inclusive=True"
                end_code = getattr(self, 'quarter_code', None)
                if end_code is None or end_code == start_code.yq:
                    end_code = start_code.yq

                self._start_code = min(start_code.yq, end_code)
                self._end_code = max(start_code.yq, end_code)

            elif n < 0:  # if counting down, _end_code becomes the _start_code
                self._end_code = start_code.yq
                self._start_code = start_code.incr(-n - 1 * inclusive, -1)

            elif n > 999:  # two yq_quarter_code values given
                end_code = YearQtr(n)
                self._start_code = min(start_code.yq, end_code.yq)
                self._end_code = max(start_code.yq, end_code.yq)

            else:  # 0 < n < 1000, so add n number of quarters
                self._start_code = start_code.yq
                self._end_code = start_code.incr(n - 1 * inclusive)

        elif hasattr(self, 'quarter_code') and not isinstance(getattr(self, 'quarter_code'), type(None)):
            self._start_code = self._end_code = self.quarter_code

        self._current_quarter_code = self.end_code
        if current_quarter:
            self.set_current_quarter_code(current_quarter)

    @property
    def start_code(self):  # earliest quarter in the time frame
        if self._start_code is None:
            self.set_time_frame()
        return self._start_code

    @property
    def end_code(self):  # latest quarter in the time frame
        if self._end_code is None:
            self.set_time_frame()
        return self._end_code

    @property
    def yq_end(self):  # a YearQtr object for easier access to YearQtr methods
        return YearQtr(self.end_code)

    @property
    def time_frame(self):  # a tuple of the two time frame end points
        return self.start_code, self.end_code

    @property
    def number_of_quarters(self):
        return dif_yq(self.end_code, self.start_code) + 1

    @property
    def time_frame_quarter_codes(self):  # a generator for all time frame quarter codes
        return YearQtr(self.start_code).quarter_codes(self.end_code)

    @property
    def time_frame_dict(self):
        # a dict of time frame codes in Iterable form
        dct = {
            'first': (self.start_code, ),
            'last': (self.end_code, ),
            'current': (self.current_quarter_code, ),
            'ends': (self.start_code, self.end_code),
            'all': self.time_frame_quarter_codes
        }

        four_qlb = self.yq_current.incr(-3)
        four_qlb_start = four_qlb if four_qlb > self.end_code else self.start_code
        annual_lb = self.yq_current.incr(-3)
        three_ylb = self.yq_current.incr(-11)
        five_ylb = self.yq_current.incr(-19)

        dct['four_quarter_lookback'] = (four_qlb, self.end_code) if four_qlb >= self.start_code else None
        dct['past_four_quarters'] = list(self.yq_current.quarter_codes(four_qlb_start))
        dct['one_year_lookback'] = (annual_lb, self.end_code) if annual_lb >= self.start_code else None
        dct['three_year_lookback'] = (three_ylb, self.end_code) if three_ylb >= self.start_code else None
        dct['five_year_lookback'] = (five_ylb, self.end_code) if five_ylb >= self.start_code else None

        for quarter_code in self.time_frame_quarter_codes:
            dct[quarter_code] = (quarter_code, )

        return dct

    def look_back_or_last(self, time_frame='four_quarter_lookback'):
        if isinstance(time_frame, int):
            start, stop = max(time_frame, self.start_code), self.end_code
        else:
            try:
                quarter_codes = self.time_frame_dict[time_frame]
                start, stop = (self.start_code, self.end_code) if quarter_codes is None \
                                  else quarter_codes[0], quarter_codes[-1]
            except KeyError:
                assert False, "Invalid key for time_frame_dict"

        return start, stop

    def get_first_last(self, time_frame):
        if isinstance(time_frame, tuple):
            first, last = time_frame[0], time_frame[-1]
        else:
            first, last = self.look_back_or_last(time_frame)
        return first, last