from __future__ import annotations

import argparse
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> str:
    coords = set()

    points, instructions = s.split('\n\n')

    for line in points.splitlines():
        x_s, y_s = line.split(',')
        coords.add((int(x_s), int(y_s)))

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

    max_x = max(x for x, _ in coords)
    max_y = max(y for _, y in coords)

    return '\n'.join(
        ''.join(
            '#' if (x, y) in coords else ' '
            for x in range(0, max_x + 1)
        )
        for y in range(0, max_y + 1)
    )


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

    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
