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
        def _read(n: int) -> int:
            nonlocal i
            ret = int(bin_str[i:i + n], 2)
            i += n
            return ret

        version = _read(3)
        type_id = _read(3)

        if type_id == 4:
            chunk = _read(5)
            n = chunk & 0b1111
            while chunk & 0b10000:
                chunk = _read(5)
                n <<= 4
                n += chunk & 0b1111

            return i, Packet(version=version, type_id=type_id, n=n)
        else:
            mode = _read(1)

            if mode == 0:
                bits_length = _read(15)
                j = i
                i = i + bits_length
                packets = []
                while j < i:
                    j, packet = parse_packet(j)
                    packets.append(packet)

                ret = Packet(
                    version=version,
                    type_id=type_id,
                    packets=tuple(packets),
                )
                return i, ret
            else:
                sub_packets = _read(11)
                packets = []
                for _ in range(sub_packets):
                    i, packet = parse_packet(i)
                    packets.append(packet)
                ret = Packet(
                    version=version,
                    type_id=type_id,
                    packets=tuple(packets),
                )
                return i, ret

    def val(packet: _Packet) -> int:
        if packet.type_id == 0:
            return sum(val(sub_packet) for sub_packet in packet.packets)
        elif packet.type_id == 1:
            res = 1
            for sub_packet in packet.packets:
                res *= val(sub_packet)
            return res
        elif packet.type_id == 2:
            return min(val(sub_packet) for sub_packet in packet.packets)
        elif packet.type_id == 3:
            return max(val(sub_packet) for sub_packet in packet.packets)
        elif packet.type_id == 4:
            return packet.n
        elif packet.type_id == 5:
            return val(packet.packets[0]) > val(packet.packets[1])
        elif packet.type_id == 6:
            return val(packet.packets[0]) < val(packet.packets[1])
        elif packet.type_id == 7:
            return val(packet.packets[0]) == val(packet.packets[1])
        else:
            raise AssertionError(packet)

    _, packet = parse_packet(0)
    return val(packet)


INPUT_S = '''\
C200B40A82
'''
EXPECTED = 3


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
