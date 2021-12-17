from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> str:
    coords = set()

    points, instructions = s.split('\n\n')

    for line in points.splitlines():
        x, y = support.parse_numbers_comma(line)
        coords.add((x, y))

    for line in instructions.splitlines():
        start, end = line.split('=')
        direction = start[-1]
        value = int(end)

        if direction == 'x':
            coords = {
                (
                    x if x < value else value - (x - value),
                    y
                )
                for x, y in coords
            }
        else:
            coords = {
                (
                    x,
                    y if y < value else value - (y - value),
                )
                for x, y in coords
            }

    return support.format_coords_hash(coords)


INPUT_S = '''\
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
'''
EXPECTED_S = '''\
#####
#   #
#   #
#   #
#####
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED_S.rstrip()),
    ),
)
def test(input_s: str, expected: str) -> None:
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
