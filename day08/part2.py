from __future__ import annotations

import argparse
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()

    total = 0
    for line in lines:
        start, end = line.split(' | ')
        end_parts = [''.join(sorted(s)) for s in end.split()]
        digits = {*start.split(), *end_parts}
        digits = {''.join(sorted(part)) for part in digits}

        num_to_s = {}
        num_to_s[1], = (s for s in digits if len(s) == 2)
        num_to_s[7], = (s for s in digits if len(s) == 3)
        num_to_s[4], = (s for s in digits if len(s) == 4)
        num_to_s[8], = (s for s in digits if len(s) == 7)
        len6 = {s for s in digits if len(s) == 6}

        num_to_s[6], = (s for s in len6 if len(set(s) & set(num_to_s[1])) == 1)
        num_to_s[9], = (s for s in len6 if len(set(s) & set(num_to_s[4])) == 4)
        num_to_s[0], = len6 - {num_to_s[6], num_to_s[9]}

        len5 = {s for s in digits if len(s) == 5}

        num_to_s[5], = (s for s in len5 if len(set(s) & set(num_to_s[6])) == 5)
        num_to_s[3], = (s for s in len5 if len(set(s) & set(num_to_s[1])) == 2)
        num_to_s[2], = len5 - {num_to_s[5], num_to_s[3]}

        s_to_num = {v: k for k, v in num_to_s.items()}

        total += sum(10 ** (3 - i) * s_to_num[end_parts[i]] for i in range(4))

    return total


INPUT_S = '''\
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
'''  # noqa: E501
EXPECTED = 61229


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
