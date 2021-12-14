from __future__ import annotations

import argparse
import collections
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    s, repls = s.split('\n\n')

    counts: collections.Counter[str] = collections.Counter()
    for i in range(0, len(s) - 1):
        counts[s[i:i + 2]] += 1

    patterns = {}
    for line in repls.splitlines():
        in_p, ins = line.split(' -> ')
        patterns[in_p] = ins

    for _ in range(40):
        counts2: collections.Counter[str] = collections.Counter()
        new_counts: collections.Counter[str] = collections.Counter()
        for k, v in counts.items():
            new_counts[f'{k[0]}{patterns[k]}'] += v
            new_counts[f'{patterns[k]}{k[1]}'] += v
            counts2[k[0]] += v
            counts2[patterns[k]] += v
        counts = new_counts

    counts2[s[-1]] += 1

    s_counts = sorted(v for v in counts2.values())
    return (s_counts[-1] - s_counts[0])


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
EXPECTED = 2188189693529


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
