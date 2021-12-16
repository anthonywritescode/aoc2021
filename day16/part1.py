from __future__ import annotations

import argparse
import os.path
from typing import NamedTuple
from typing import Protocol

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class _Packet(Protocol):
    @property
    def version(self) -> int: ...
    @property
    def type_id(self) -> int: ...
    @property
    def n(self) -> int: ...
    @property
    def packets(self) -> tuple[_Packet, ...]: ...


class Packet(NamedTuple):
    version: int
    type_id: int
    n: int = -1
    packets: tuple[_Packet, ...] = ()


def compute(s: str) -> int:
    bin_str = ''
    for c in s.strip():
        bin_str += f'{int(c, 16):04b}'

    def parse_packet(i: int) -> tuple[int, _Packet]:
        version_id = int(bin_str[i:i + 3], 2)
        i += 3
        type_id = int(bin_str[i:i + 3], 2)
        i += 3

        if type_id == 4:
            n = 0
            # literal
            chunk = bin_str[i:i + 5]
            i += 5
            n += int(chunk[1:], 2)
            while chunk[0] == '1':
                chunk = bin_str[i:i + 5]
                i += 5
                n <<= 4
                n += int(chunk[1:], 2)

            return i, Packet(version=version_id, type_id=type_id, n=n)
        else:
            mode = int(bin_str[i], 2)
            i += 1

            if mode == 0:
                bits_length = int(bin_str[i:i + 15], 2)
                i += 15
                j = i
                i = i + bits_length
                packets = []
                while j < i:
                    j, packet = parse_packet(j)
                    packets.append(packet)

                ret = Packet(
                    version=version_id,
                    type_id=type_id,
                    packets=tuple(packets),
                )
                return i, ret
            else:
                sub_packets = int(bin_str[i:i + 11], 2)
                i += 11
                packets = []
                for _ in range(sub_packets):
                    i, packet = parse_packet(i)
                    packets.append(packet)
                ret = Packet(
                    version=version_id,
                    type_id=type_id,
                    packets=tuple(packets),
                )
                return i, ret

    _, packet = parse_packet(0)
    todo = [packet]
    total = 0
    while todo:
        item = todo.pop()
        total += item.version
        todo.extend(item.packets)

    return total


INPUT_S = '''\
8A004A801A8002F478
'''
EXPECTED = 16


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
