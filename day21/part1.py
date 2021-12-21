from __future__ import annotations

import argparse
import itertools
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def weird_mod(n: int) -> int:
    while n > 10:
        n -= 10
    return n


def compute(s: str) -> int:
    lines = s.splitlines()
    _, _, _, _, p0_s = lines[0].split()
    _, _, _, _, p1_s = lines[1].split()
    p1, p2 = int(p0_s), int(p1_s)

    die_count = 0
    die = itertools.cycle(range(1, 101))
    p1_score = p2_score = 0

    while True:
        p1 = weird_mod(p1 + next(die) + next(die) + next(die))
        die_count += 3
        p1_score += p1

        if p1_score >= 1000:
            break

        p2 = weird_mod(p2 + next(die) + next(die) + next(die))
        die_count += 3
        p2_score += p2

        if p2_score >= 1000:
            break

    return die_count * min(p1_score, p2_score)


INPUT_S = '''\
Player 1 starting position: 4
Player 2 starting position: 8
'''
EXPECTED = 739785


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
