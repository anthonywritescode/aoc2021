from __future__ import annotations

import argparse
import os.path
from typing import Generator

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def adjacent(x: int, y: int) -> Generator[tuple[int, int], None, None]:
    for x_d in (-1, 0, 1):
        for y_d in (-1, 0, 1):
            if x_d == y_d == 0:
                continue
            yield x + x_d, y + y_d


def compute(s: str) -> int:
    coords = {}
    for y, line in enumerate(s.splitlines()):
        for x, c in enumerate(line):
            coords[(x, y)] = int(c)

    flashes = 0
    for _ in range(100):
        todo = []
        for pt in coords:
            coords[pt] += 1
            if coords[pt] > 9:
                todo.append(pt)

        while todo:
            flashing = todo.pop()
            if coords[flashing] == 0:
                continue
            coords[flashing] = 0
            flashes += 1
            for pt in adjacent(*flashing):
                if pt in coords and coords[pt] != 0:
                    coords[pt] += 1
                    if coords[pt] > 9:
                        todo.append(pt)

    return flashes


INPUT_S = '''\
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
'''
EXPECTED = 1656


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
