from __future__ import annotations

import argparse
import os.path
import statistics

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    numbers = support.parse_numbers_comma(s)

    def get_val(n: int) -> int:
        return sum(abs(num - n) * (abs(num - n) + 1) // 2 for num in numbers)

    mean = round(statistics.mean(numbers))
    val = get_val(mean)

    if get_val(mean - 1) < val:
        direction = -1
    else:
        direction = 1

    while get_val(mean + direction) < val:
        mean += direction
        val = get_val(mean)

    return val


INPUT_S = '''\
16,1,2,0,4,2,7,1,2,14
'''
EXPECTED = 168


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
