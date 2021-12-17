from __future__ import annotations

import argparse
import os.path
from typing import Any

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()

    columns = list(zip(*lines))

    path: list[str] = []
    included = set(range(len(lines)))
    while len(included) != 1:
        column = columns[len(path)]
        ones = sum(column[pos] == '1' for pos in included)
        if ones >= len(included) / 2:
            path.append('1')
        else:
            path.append('0')

        included = {pos for pos in included if column[pos] == path[-1]}

    best = lines[next(iter(included))]

    path = []
    included = set(range(len(lines)))
    while len(included) != 1:
        column = columns[len(path)]
        ones = sum(column[pos] == '1' for pos in included)
        if ones < len(included) / 2:
            path.append('1')
        else:
            path.append('0')

        included = {pos for pos in included if column[pos] == path[-1]}

    worst = lines[next(iter(included))]

    return int(best, 2) * int(worst, 2)


def compute_haxy_dicts(s: str) -> int:
    lines = s.splitlines()

    root: dict[str, Any] = {'count': 0}
    for line in lines:
        current = root
        for c in line:
            current['count'] += 1
            current.setdefault(c, {'count': 0})
            current = current[c]
        current['count'] += 1

    path = []
    current = root
    while True:
        if (
                current.get('1', {}).get('count', 0) >=
                current.get('0', {}).get('count', 0)
        ):
            current = current['1']
            path.append('1')
        else:
            current = current['0']
            path.append('0')

        if current['count'] == 1:
            prefix = ''.join(path)
            break

    path = []
    current = root
    while True:
        if (
                current.get('1', {}).get('count', 0) <
                current.get('0', {}).get('count', 0)
        ):
            current = current['1']
            path.append('1')
        else:
            current = current['0']
            path.append('0')

        if current['count'] == 1:
            prefix2 = ''.join(path)
            break

    best, = (line for line in lines if line.startswith(prefix))
    worst, = (line for line in lines if line.startswith(prefix2))

    return int(best, 2) * int(worst, 2)


INPUT_S = '''\
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 230),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing('haxy dicts'):
        print(compute_haxy_dicts(f.read()))

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
