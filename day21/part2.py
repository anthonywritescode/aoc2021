from __future__ import annotations

import argparse
import functools
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

    @functools.lru_cache(maxsize=None)
    def compute_win_count(
            p1_pos: int,
            p1_score: int,
            p2_pos: int,
            p2_score: int,
            p1_turn: bool,
    ) -> tuple[int, int]:
        if p1_turn:
            p1_wins = p2_wins = 0
            for i, j, k in itertools.product((1, 2, 3), (1, 2, 3), (1, 2, 3)):
                new_p1_pos = weird_mod(p1_pos + i + j + k)
                new_p1_score = p1_score + new_p1_pos
                if new_p1_score >= 21:
                    p1_wins += 1
                else:
                    tmp_p1_wins, tmp_p2_wins = compute_win_count(
                        new_p1_pos,
                        new_p1_score,
                        p2_pos,
                        p2_score,
                        p1_turn=False,
                    )
                    p1_wins += tmp_p1_wins
                    p2_wins += tmp_p2_wins

            return p1_wins, p2_wins
        else:
            p1_wins = p2_wins = 0
            for i, j, k in itertools.product((1, 2, 3), (1, 2, 3), (1, 2, 3)):
                new_p2_pos = weird_mod(p2_pos + i + j + k)
                new_p2_score = p2_score + new_p2_pos
                if new_p2_score >= 21:
                    p2_wins += 1
                else:
                    tmp_p1_wins, tmp_p2_wins = compute_win_count(
                        p1_pos,
                        p1_score,
                        new_p2_pos,
                        new_p2_score,
                        p1_turn=True,
                    )
                    p1_wins += tmp_p1_wins
                    p2_wins += tmp_p2_wins

            return p1_wins, p2_wins

    p1_win, p2_win = compute_win_count(p1, 0, p2, 0, p1_turn=True)
    return max(p1_win, p2_win)


INPUT_S = '''\
Player 1 starting position: 4
Player 2 starting position: 8
'''
EXPECTED = 444356092776315


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
