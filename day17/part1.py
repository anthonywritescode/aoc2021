from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    _, _, x_s, y_s = s.split()
    x_s = x_s[2:-1]
    y_s = y_s[2:]

    y1_s, _ = y_s.split('..')
    y1 = int(y1_s)

    y0 = abs(y1) - 1  # also t!

    return y0 * y0 - (y0 - 1) * y0 // 2


INPUT_S = '''\
target area: x=20..30, y=-10..-5
'''
EXPECTED = 45


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
