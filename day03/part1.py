from __future__ import annotations

import argparse
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()

    counts = [0] * len(lines[0])

    for line in lines:
        for i, c in enumerate(line):
            if c == '1':
                counts[i] += 1

    gamma = 0
    eps = 0
    for i in range(len(lines[0])):
        gamma <<= 1
        eps <<= 1
        if counts[i] > len(lines) // 2:
            gamma += 1
        else:
            eps += 1

    return gamma * eps


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
        (INPUT_S, 198),
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
