from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

POINTS = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}
FORWARD = {'{': '}', '(': ')', '[': ']', '<': '>'}
REVERSE = {v: k for k, v in FORWARD.items()}


def compute(s: str) -> int:
    total = 0
    lines = s.splitlines()
    for line in lines:
        stack = []
        for c in line:
            if c in FORWARD:
                stack.append(c)
            elif c in REVERSE:
                if stack[-1] != REVERSE[c]:
                    total += POINTS[c]
                    break
                else:
                    stack.pop()
    return total


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
EXPECTED = 26397


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
