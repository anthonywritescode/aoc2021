from __future__ import annotations

import argparse
import ast
import math
import os.path
import re
from typing import Any
from typing import Match

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

PAIR_RE = re.compile(r'\[(\d+),(\d+)\]')
NUM_LEFT_RE = re.compile(r'\d+(?!.*\d)')
NUM_RE = re.compile(r'\d+')
GT_10 = re.compile(r'\d\d+')


def add_number(s1: str, s2: str) -> str:
    return f'[{s1},{s2}]'


def reduce_number(s: str) -> str:
    while True:
        continue_outer = False
        for pair in PAIR_RE.finditer(s):
            before = s[:pair.start()]
            if before.count('[') - before.count(']') >= 4:
                def left_cb(match: Match[str]) -> str:
                    return str(int(match[0]) + int(pair[1]))

                def right_cb(match: Match[str]) -> str:
                    return str(int(match[0]) + int(pair[2]))

                start = NUM_LEFT_RE.sub(left_cb, s[:pair.start()], count=1)
                end = NUM_RE.sub(right_cb, s[pair.end():], count=1)
                s = f'{start}0{end}'

                continue_outer = True
                break

        if continue_outer:
            continue

        gt_10_match = GT_10.search(s)
        if gt_10_match:
            def match_cb(match: Match[str]) -> str:
                val = int(match[0])
                return f'[{math.floor(val/2)},{math.ceil(val/2)}]'

            s = GT_10.sub(match_cb, s, count=1)
            continue

        return s


def compute_sum(s: str) -> int:
    def compute_val(v: int | Any) -> int:
        if isinstance(v, int):
            return v
        else:
            assert len(v) == 2
            return 3 * compute_val(v[0]) + 2 * compute_val(v[1])

    return compute_val(ast.literal_eval(s))


def compute(s: str) -> int:
    lines = s.splitlines()

    maximum = 0
    for i, line in enumerate(lines):
        for j, other in enumerate(lines[i + 1:], start=i + 1):
            maximum = max(
                maximum,
                compute_sum(reduce_number(add_number(line, other))),
            )
            maximum = max(
                maximum,
                compute_sum(reduce_number(add_number(other, line))),
            )

    return maximum


INPUT_S = '''\
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
'''
EXPECTED = 3993


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
