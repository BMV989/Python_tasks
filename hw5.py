#!/usr/bin/env python3

import unittest
import re
from datetime import datetime, date
from collections import OrderedDict

RE_TIME = re.compile(r'.*\[(.+?) [\+-].*?')


def merge(*iterables: iter, key=None) -> iter:
    """Функция склеивает упорядоченные по ключу `key` и порядку «меньше»
    коллекции из `iterables`.

    Результат — итератор на упорядоченные данные.
    В случае равенства данных следует их упорядочить в порядке следования
    коллекций"""
    if not key:
        def key(x): return x

    els = OrderedDict()
    for i in iterables:
        si = iter(sorted(i, key=key))
        try:
            els[si] = next(si)
        except StopIteration:
            pass

    while els:
        res = min(els.items(), key=lambda x: key(x[1]))
        yield res[1]
        try:
            els[res[0]] = next(res[0])
        except StopIteration:
            del els[res[0]]


def log_key(s: str) -> date | float:
    """Функция по строке лога возвращает ключ для её сравнения по времени"""
    time = RE_TIME.search(s)
    if time is not None:
        return datetime.strptime(time.group(1), '%d/%b/%Y:%H:%M:%S')
    return float("+inf")


class TestTest(unittest.TestCase):
    def test_log_right(self):
        t_string = '--[17/Feb/2013:06:37:21 +0600]'
        self.assertEqual(datetime(
            2013, 2, 17, 6, 37, 21), log_key(t_string))

    def test_log_right_with_minus(self):
        t_string = '--[17/Feb/2013:06:37:21 -0600]'
        self.assertEqual(datetime(
            2013, 2, 17, 6, 37, 21), log_key(t_string))

    def test_log_wrong(self):
        t_string = '--[ffffffvvv'
        self.assertEqual(float("+inf"), log_key(t_string))

    def test_iter_works(self):
        i1 = [1, 2, 4]
        i2 = [3, 5]
        res = [1, 2, 3, 4, 5]
        i = 0
        for e in merge(i1, i2):
            self.assertEqual(res[i], e)
            i += 1

    def test_iter_works_with_eq(self):
        i1 = [1, 2, 4]
        i2 = [1, 5]
        res = [1, 1, 2, 4, 5]
        i = 0
        for e in merge(i1, i2):
            self.assertEqual(res[i], e)
            i += 1

    def test_iter_works_with_str(self):
        i1 = ["c", "b", "a"]
        i2 = ["e", "d"]
        res = ["a", "b", "c", "d", "e"]
        i = 0
        for e in merge(i1, i2):
            self.assertEqual(res[i], e)
            i += 1

    def test_iter_works_with_str_eq(self):
        i1 = ["c", "b", "a"]
        i2 = ["c", "d"]
        res = ["a", "b", "c", "c", "d"]
        i = 0
        for e in merge(i1, i2):
            self.assertEqual(res[i], e)
            i += 1

    def test_saves_order_seconds(self):
        a = ' [09/Dec/2023:10:00:00 +0600] '
        b = ' [09/Dec/2023:10:00:15 +0600] '

        assert log_key(a) < log_key(b)

    def test_saves_order_days(self):
        a = ' [10/Dec/2023:10:00:00 +0600] '
        b = ' [09/Dec/2023:10:00:00 +0600] '

        assert log_key(a) > log_key(b)

    def test_all(self):
        a = ' [09/Dec/2023:10:00:00 +0600] '
        b = ' [10/Dec/2023:10:00:00 +0600] '
        c = ' [08/Dec/2023:10:00:00 +0600] '
        d = ' [11/Dec/2023:10:00:00 +0600] '

        h = merge([a, b], [c, d], key=log_key)

        assert [c, a, b, d] == list(h)


if __name__ == "__main__":
    pass
