from __future__ import annotations

import argparse
import collections
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    edges = collections.defaultdict(set)
    for line in s.splitlines():
        src, dst = line.split('-')
        edges[src].add(dst)
        edges[dst].add(src)

    done = set()

    todo: list[tuple[tuple[str, ...], bool]] = [(('start',), False)]
    while todo:
        path, double_small = todo.pop()
        if path[-1] == 'end':
            done.add(path)
            continue

        for choice in edges[path[-1]] - {'start'}:
            if choice.isupper():
                todo.append(((*path, choice), double_small))
            elif double_small is False and path.count(choice) == 1:
                todo.append(((*path, choice), True))
            elif choice not in path:
                todo.append(((*path, choice), double_small))

    return len(done)


INPUT_S = '''\
start-A
start-b
A-c
A-b
b-d
A-end
b-end
'''
EXPECTED = 36
INPUT_2 = '''\
dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
        (INPUT_2, 103),
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
