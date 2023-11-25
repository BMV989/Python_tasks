#!/usr/bin/env python3


def long_division(dividend: int, divider: int) -> str:
    """
    Вернуть строку с процедурой деления «уголком» чисел dividend и divider.
    Формат вывода приведён на примерах ниже.

    Примеры:
    >>> 12345÷25
    12345|25
    100  |493
     234
     225
       95
       75
       20

    >>> 1234÷1423
    1234|1423
    1234|0

    >>> 24600÷123
    24600|123
    246  |200
      0

    >>> 246001÷123
    246001|123
    246   |2000
         1
    """
    # INSERT CODE HERE
    ans = f"{dividend}|{divider}\n"
    q = dividend // divider
    q_str = str(q)
    if q == 0:
        return ans + f"{dividend}|{q}"
    s = int(q_str[0]) * divider
    ptr = len(str(dividend)) - len(str(s))
    su = dividend // 10**ptr
    if su < s:
        su = dividend // 10 ** (ptr - 1)
    another_spaces = " " * (len(str(su)) - len(str(s)))
    r_spaces = " " * (len(str(dividend)) - len(str(s)) - len(another_spaces))
    l_spaces = ""
    ans += f"{another_spaces}{s}{r_spaces}|{q}\n"
    left = str(dividend)[len(str(su)):]
    su -= s
    q_str = q_str[1:]
    while len(q_str) != 0:
        if q_str[0] == "0":
            q_str = q_str[1:]
            continue
        s = int(q_str[0]) * divider
        r_spaces = " " * (len(q_str[1:]))
        while su < divider:
            su = int(f"{su}{left[0]}")
            left = left[1:]
        l_spaces = " " * (len(str(dividend)) - len(r_spaces) - len(str(su)))
        another_spaces = " " * (len(str(su)) - len(str(s)))
        ans += f"{l_spaces}{su}\n"
        ans += f"{l_spaces}{another_spaces}{s}\n"
        su -= s
        q_str = q_str[1:]
    if dividend % divider == 0:
        another_spaces = " " * (len(str(s)) - len(str(dividend % divider)))
        ans += f"{l_spaces}{another_spaces}{dividend % divider}"
    else:
        l_spaces = " " * (len(str(dividend)) - len(str(dividend % divider)))
        ans += f"{l_spaces}{dividend % divider}"
    return ans


def main():
    print(long_division(123, 123))
    print()
    print(long_division(1, 1))
    print()
    print(long_division(15, 3))
    print()
    print(long_division(3, 15))
    print()
    print(long_division(12345, 25))
    print()
    print(long_division(1234, 1423))
    print()
    print(long_division(87654532, 1))
    print()
    print(long_division(24600, 123))
    print()
    print(long_division(4567, 1234567))
    print()
    print(long_division(246001, 123))
    print()
    print(long_division(100000, 50))
    print()
    print(long_division(123456789, 531))
    print()
    print(long_division(425934261694251, 12345678))


if __name__ == "__main__":
    main()
