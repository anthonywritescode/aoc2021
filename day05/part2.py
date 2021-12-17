from __future__ import annotations

import argparse
import collections
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    positions: collections.Counter[tuple[int, int]] = collections.Counter()
    lines = s.splitlines()
    for line in lines:
        p1, p2 = line.split(' -> ')
        x1, y1 = support.parse_numbers_comma(p1)
        x2, y2 = support.parse_numbers_comma(p2)

        if x2 > x1:
            x_d = 1
        elif x2 < x1:
            x_d = -1
        else:
            x_d = 0

        if y2 > y1:
            y_d = 1
        elif y2 < y1:
            y_d = -1
        else:
            y_d = 0

        x, y = x1, y1
        while (x, y) != (x2, y2):
            positions[(x, y)] += 1
            x, y = x + x_d, y + y_d
        positions[(x2, y2)] += 1

    n = 0
    for k, v in positions.most_common():
        if v > 1:
            n += 1
        else:
            break
    return n


INPUT_S = '''\
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
'''
EXPECTED = 12


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
