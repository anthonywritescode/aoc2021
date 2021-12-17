from __future__ import annotations

import argparse
import heapq
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    coords = support.parse_coords_int(s)

    end = max(coords)

    best_at: dict[tuple[int, int], int] = {}

    todo = [(0, (0, 0))]
    while todo:
        cost, last_coord = heapq.heappop(todo)

        if last_coord in best_at and cost >= best_at[last_coord]:
            continue
        else:
            best_at[last_coord] = cost

        if last_coord == end:
            return cost

        for cand in support.adjacent_4(*last_coord):
            if cand in coords:
                heapq.heappush(todo, (cost + coords[cand], cand))

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
EXPECTED = 40


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
