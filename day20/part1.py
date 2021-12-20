from __future__ import annotations

import argparse
import collections
import functools
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def to_int(coords: dict[tuple[int, int], int], x: int, y: int) -> int:
    numbers = [
        coords[x-1, y-1], coords[x, y-1], coords[x+1, y-1],
        coords[x-1, y], coords[x, y], coords[x+1, y],
        coords[x-1, y+1], coords[x, y+1], coords[x+1, y+1],
    ]
    return int(''.join(str(int(n)) for n in numbers), 2)


def compute(s: str) -> int:
    p1, p2 = s.split('\n\n')

    part1 = collections.defaultdict(int)
    for i, c in enumerate(p1.strip()):
        if c == '#':
            part1[i] = 1

    part2_coords_s = support.parse_coords_hash(p2)
    part2_coords_d = collections.defaultdict(
        int,
        dict.fromkeys(part2_coords_s, 1),
    )

    for i in range(2):
        minx = min(x for x, _ in part2_coords_d)
        maxx = max(x for x, _ in part2_coords_d)
        miny = min(y for _, y in part2_coords_d)
        maxy = max(y for _, y in part2_coords_d)

        if part1[0] == 1 and part1[511] == 0:
            new_coords: collections.defaultdict[tuple[int, int], int]
            new_coords = collections.defaultdict(
                functools.partial(lambda q: int(q % 2 == 0), q=i),
            )
        else:
            new_coords = collections.defaultdict(int)
        for y in range(miny - 1, maxy + 2):
            for x in range(minx - 1, maxx + 2):
                if part1[to_int(part2_coords_d, x, y)]:
                    new_coords[(x, y)] = 1
                else:
                    new_coords[(x, y)] = 0

        part2_coords_d = new_coords

    return sum(part2_coords_d.values())


INPUT_S = '''\
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
'''
EXPECTED = 35


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
