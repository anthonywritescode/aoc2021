from __future__ import annotations

import argparse
import collections
import os.path
import sys

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    coords = collections.defaultdict(lambda: sys.maxsize)

    lines = s.splitlines()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            coords[(y, x)] = int(c)

    total = 0
    for (y, x), n in tuple(coords.items()):
        if (
            coords[y, x + 1] > n and
            coords[y, x - 1] > n and
            coords[y + 1, x] > n and
            coords[y - 1, x] > n
        ):
            total += n + 1

    return total


INPUT_S = '''\
2199943210
3987894921
9856789892
8767896789
9899965678
'''
EXPECTED = 15


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

    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
