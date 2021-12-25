from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    coords: dict[tuple[int, int], support.Direction4] = {}
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == 'v':
                coords[(x, y)] = support.Direction4.DOWN
            elif c == '>':
                coords[(x, y)] = support.Direction4.RIGHT

    i = 0
    while True:
        i += 1

        new_coords_1: dict[tuple[int, int], support.Direction4] = {}
        for (x, y), direction in coords.items():
            if direction is support.Direction4.RIGHT:
                new_x, new_y = direction.apply(x, y)
                new_x %= len(lines[0])
                new_y %= len(lines)
                if (new_x, new_y) not in coords:
                    new_coords_1[(new_x, new_y)] = direction
                else:
                    new_coords_1[(x, y)] = direction
            else:
                new_coords_1[(x, y)] = direction

        new_coords_2: dict[tuple[int, int], support.Direction4] = {}
        for (x, y), direction in new_coords_1.items():
            if direction is support.Direction4.DOWN:
                new_x, new_y = direction.apply(x, y)
                new_x %= len(lines[0])
                new_y %= len(lines)
                if (new_x, new_y) not in new_coords_1:
                    new_coords_2[(new_x, new_y)] = direction
                else:
                    new_coords_2[(x, y)] = direction
            else:
                new_coords_2[(x, y)] = direction

        if new_coords_2 == coords:
            break
        else:
            coords = new_coords_2

    return i


INPUT_S = '''\
v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>
'''
EXPECTED = 58


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
