__author__ = 'cole'

import unittest

from year_quarter import dif_yq, incr_yq, count_yq
from year_quarter import YearQtr


class YearQtrTestCase(unittest.TestCase):
    def test_incr_yq(self):
        self.assertEqual(incr_yq(20141, 1), 20142)
        self.assertEqual(incr_yq(20144, 1), 20151)
        self.assertEqual(incr_yq(20141, 4), 20151)
        self.assertEqual(incr_yq(20142, 3), 20151)
        self.assertEqual(incr_yq(20143, 2), 20151)
        self.assertEqual(incr_yq(20141, 9), 20162)

        self.assertEqual(incr_yq(20144, -1), 20143)
        self.assertEqual(incr_yq(20141, -1), 20134)
        self.assertEqual(incr_yq(20144, -4), 20134)
        self.assertEqual(incr_yq(20143, -3), 20134)
        self.assertEqual(incr_yq(20142, -2), 20134)
        self.assertEqual(incr_yq(20141, -7), 20122)

        self.assertEqual(incr_yq(20141, 0), 20141)
        self.assertEqual(incr_yq(20146, 0), 20152)

    def test_dif_yq(self):
        self.assertEqual(dif_yq(20144, 20143), 1)
        self.assertEqual(dif_yq(20151, 20144), 1)
        self.assertEqual(dif_yq(20143, 20144), -1)
        self.assertEqual(dif_yq(20144, 20151), -1)

    def test_yc_count(self):
        yqg = count_yq(20141)
        self.assertEqual(yqg.next(), 20141)
        self.assertEqual(yqg.next(), 20142)
        self.assertEqual(yqg.next(), 20143)
        self.assertEqual(yqg.next(), 20144)
        self.assertEqual(yqg.next(), 20151)

        yqg = count_yq(20141, 3)
        self.assertEqual(list(yqg), [20141, 20142, 20143])

        yqg = count_yq(20141, 20152)
        self.assertEqual(list(yqg), [20141, 20142, 20143, 20144, 20151])

        yqg = count_yq(20141, None, -1)
        self.assertEqual(yqg.next(), 20141)
        self.assertEqual(yqg.next(), 20134)

        yqg = count_yq(20141, -3)
        self.assertEqual(list(yqg), [20133, 20134, 20141])

        yqg = count_yq(20141, 3, -1)
        self.assertEqual(list(yqg), [20141, 20134, 20133])


class YearQuarterTestCase(unittest.TestCase):
    def test_yq(self):
        yq = YearQtr(20141)
        self.assertEqual(yq.yq, 20141)
        self.assertEqual(yq.year, 2014)
        self.assertEqual(yq.qtr, 1)
        self.assertEqual(YearQtr(20145).yq, 20151)
        self.assertEqual(yq.incr(10), incr_yq(20141, 10))
        self.assertEqual(yq.dif(20152), dif_yq(20141, 20152))