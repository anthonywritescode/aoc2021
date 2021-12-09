from __future__ import annotations

import argparse
import collections
import os.path
from typing import Generator

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def adjacent(y: int, x: int) -> Generator[tuple[int, int], None, None]:
    yield y, x + 1
    yield y, x - 1
    yield y - 1, x
    yield y + 1, x


def compute(s: str) -> int:
    coords = collections.defaultdict(lambda: 9)

    lines = s.splitlines()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            coords[(y, x)] = int(c)

    sizes = []
    for (y, x), n in tuple(coords.items()):
        if all(coords[pt] > n for pt in adjacent(y, x)):
            seen = set()
            todo = [(y, x)]
            while todo:
                y, x = todo.pop()
                seen.add((y, x))

                for other in adjacent(y, x):
                    if other not in seen and coords[other] != 9:
                        todo.append(other)

            sizes.append(len(seen))

    sizes.sort()
    return sizes[-1] * sizes[-2] * sizes[-3]


INPUT_S = '''\
2199943210
3987894921
9856789892
8767896789
9899965678
'''
EXPECTED = 1134


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
