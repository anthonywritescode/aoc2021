from __future__ import annotations

import argparse
import heapq
import os.path
from typing import Generator

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def next_p(x: int, y: int) -> Generator[tuple[int, int], None, None]:
    yield x - 1, y
    yield x, y - 1
    yield x + 1, y
    yield x, y + 1


def weird_mod(n: int) -> int:
    while n > 9:
        n -= 9
    return n


def compute(s: str) -> int:
    coords = {}
    lines = s.splitlines()
    width = len(lines[0])
    height = len(lines)

    for y, line in enumerate(s.splitlines()):
        for x, c in enumerate(line):
            for y_i in range(5):
                for x_i in range(5):
                    coords[(x_i * height + x, y_i * width + y)] = (
                        weird_mod(int(c) + x_i + y_i)
                    )

    last_x, last_y = max(coords)

    best_at: dict[tuple[int, int], int] = {}

    todo = [(0, (0, 0))]
    while todo:
        cost, last_coord = heapq.heappop(todo)

        if last_coord in best_at and cost >= best_at[last_coord]:
            continue
        else:
            best_at[last_coord] = cost

        if last_coord == (last_x, last_y):
            return cost

        for cand in next_p(*last_coord):
            if cand in coords:
                todo.append((cost + coords[cand], cand))

    raise AssertionError('unreachable')


INPUT_S = '''\
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
'''
EXPECTED = 315


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
