from __future__ import annotations

import argparse
import os.path
from typing import NamedTuple

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class Reboot(NamedTuple):
    on: bool
    x: tuple[int, int]
    y: tuple[int, int]
    z: tuple[int, int]

    @classmethod
    def parse(cls, s: str) -> Reboot:
        status, rest = s.split()
        x, y, z = rest.split(',')
        x, y, z = x[2:], y[2:], z[2:]
        x_0_s, x_1_s = x.split('..')
        y_0_s, y_1_s = y.split('..')
        z_0_s, z_1_s = z.split('..')

        return cls(
            status == 'on',
            (int(x_0_s), int(x_1_s)),
            (int(y_0_s), int(y_1_s)),
            (int(z_0_s), int(z_1_s)),
        )


def compute(s: str) -> int:
    reboots = [Reboot.parse(line) for line in s.splitlines()]

    coords = set()
    for step in reboots:
        new_coords = {
            (x, y, z)
            for x in range(max(step.x[0], -50), min(step.x[1], 50) + 1)
            for y in range(max(step.y[0], -50), min(step.y[1], 50) + 1)
            for z in range(max(step.z[0], -50), min(step.z[1], 50) + 1)
        }

        if step.on:
            coords |= new_coords
        else:
            coords -= new_coords

    return len(coords)


INPUT_S = '''\
on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682
'''
EXPECTED = 590784


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
