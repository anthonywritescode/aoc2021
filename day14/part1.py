from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    s, repls = s.split('\n\n')

    patterns = {}
    for line in repls.splitlines():
        in_p, ins = line.split(' -> ')
        patterns[in_p] = ins

    for i in range(10):
        next_s: list[str] = []
        for i, c in enumerate(s):
            cand = s[i:i + 2]
            if cand in patterns:
                next_s.extend((c, patterns[cand]))
            else:
                next_s.append(c)
        s = ''.join(next_s)

    counts = {
        k: s.count(k)
        for k in set(patterns.values())
    }
    s_counts = sorted(v for k, v in counts.items())
    return s_counts[-1] - s_counts[0]


INPUT_S = '''\
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
'''
EXPECTED = 1588


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
