from __future__ import annotations

import argparse
import heapq
import os.path
from typing import Generator
from typing import NamedTuple

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

POS = {'A': 0, 'B': 1, 'C': 2, 'D': 3}


class State(NamedTuple):
    top: dict[int, int | None]
    row1: dict[int, int | None]
    row2: dict[int, int | None]

    def __hash__(self) -> int:
        return hash((
            tuple(self.top.items()),
            tuple(self.row1.items()),
            tuple(self.row2.items()),
        ))

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, State):
            return NotImplemented
        else:
            return id(self) < id(other)

    @property
    def completed(self) -> bool:
        return (
            all(k == v for k, v in self.row1.items()) and
            all(k == v for k, v in self.row2.items())
        )

    @classmethod
    def parse(cls, s: str) -> State:
        lines = s.splitlines()
        return cls(
            dict.fromkeys((1, 3, 5, 7, 9), None),
            {
                0: POS[lines[2][3]],
                1: POS[lines[2][5]],
                2: POS[lines[2][7]],
                3: POS[lines[2][9]],
            },
            {
                0: POS[lines[3][3]],
                1: POS[lines[3][5]],
                2: POS[lines[3][7]],
                3: POS[lines[3][9]],
            },
        )

    def __repr__(self) -> str:
        return (
            f'State(\n'
            f'    top={self.top!r},\n'
            f'    row1={self.row1!r},\n'
            f'    row2={self.row2!r},\n'
            f')'
        )


def next_states(
        score: int,
        state: State,
) -> Generator[tuple[int, State], None, None]:
    for k, v in state.top.items():
        if v is None:
            continue

        target_col = 2 + v * 2
        max_c = max(target_col, k)
        min_c = min(target_col, k)
        to_move_top = max_c - min_c

        if all(
            k2 <= min_c or k2 >= max_c or v2 is None
            for k2, v2 in state.top.items()
        ):
            if state.row2[v] is None:
                yield (
                    score + (to_move_top + 2) * 10 ** v,
                    state._replace(
                        top={**state.top, k: None},
                        row2={**state.row2, v: v},
                    )
                )
            elif state.row2[v] == v and state.row1[v] is None:
                yield (
                    score + (to_move_top + 1) * 10 ** v,
                    state._replace(
                        top={**state.top, k: None},
                        row1={**state.row1, v: v},
                    ),
                )

    potential_targets = {k for k, v in state.top.items() if v is None}
    for i in range(4):
        row1_val = state.row1[i]
        row2_val = state.row2[i]
        # this row is done! do not move!
        if row1_val == i and row2_val == i:
            continue

        for target in potential_targets:
            src_col = 2 + i * 2
            max_c = max(src_col, target)
            min_c = min(src_col, target)
            to_move_top = max_c - min_c

            if all(
                k2 <= min_c or k2 >= max_c or v2 is None
                for k2, v2 in state.top.items()
            ):
                if row1_val is not None:
                    yield (
                        score + (to_move_top + 1) * 10 ** row1_val,
                        state._replace(
                            top={**state.top, target: row1_val},
                            row1={**state.row1, i: None},
                        )
                    )
                elif row2_val != i and row2_val is not None:
                    yield (
                        score + (to_move_top + 2) * 10 ** row2_val,
                        state._replace(
                            top={**state.top, target: row2_val},
                            row2={**state.row2, i: None},
                        ),
                    )


def compute(s: str) -> int:
    initial = State.parse(s)

    best_at: dict[State, int] = {}
    todo = [(0, initial)]
    while todo:
        score, state = heapq.heappop(todo)

        best_score = best_at.setdefault(state, score)
        if best_score < score:
            continue

        if state.completed:
            return score

        for tp in next_states(score, state):
            heapq.heappush(todo, tp)

    raise AssertionError('unreachable!')


INPUT_S = '''\
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
'''
EXPECTED = 12521


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
