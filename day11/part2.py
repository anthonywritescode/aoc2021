from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    coords = support.parse_coords_int(s)

    step = 0
    while True:
        step += 1
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
            for pt in support.adjacent_8(*flashing):
                if pt in coords and coords[pt] != 0:
                    coords[pt] += 1
                    if coords[pt] > 9:
                        todo.append(pt)

        if all(val == 0 for val in coords.values()):
            return step

    raise AssertionError('unreachable')


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
EXPECTED = 195


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
