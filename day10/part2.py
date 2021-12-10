from __future__ import annotations

import argparse
import os.path
import statistics

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

POINTS = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}
FORWARD = {'{': '}', '(': ')', '[': ']', '<': '>'}
REVERSE = {v: k for k, v in FORWARD.items()}


def compute(s: str) -> int:
    scores = []
    lines = s.splitlines()
    for line in lines:
        stack = []
        for c in line:
            if c in FORWARD:
                stack.append(c)
            elif c in REVERSE:
                if stack[-1] != REVERSE[c]:
                    break
                else:
                    stack.pop()
        else:
            score = 0
            for c in reversed(stack):
                score *= 5
                score += POINTS[FORWARD[c]]
            scores.append(score)

    return int(statistics.median(scores))


INPUT_S = '''\
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
'''
EXPECTED = 288957


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
