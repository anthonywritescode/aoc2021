from __future__ import annotations

import argparse
import collections
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    numbers = collections.Counter(int(line) for line in s.strip().split(','))

    for d in range(80):
        numbers2 = collections.Counter({8: numbers[0], 6: numbers[0]})
        numbers2.update({k - 1: v for k, v in numbers.items() if k > 0})
        numbers = numbers2

    return sum(numbers.values())


INPUT_S = '''\
3,4,3,1,2
'''
EXPECTED = 5934


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
