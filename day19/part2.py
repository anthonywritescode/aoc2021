from __future__ import annotations

import argparse
import collections
import os.path
from typing import NamedTuple

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class Scanner(NamedTuple):
    sid: int
    points: list[tuple[int, int, int]]

    @classmethod
    def from_str(cls, s: str) -> Scanner:
        lines = s.splitlines()
        _, _, sid_s, _ = lines[0].split()
        points = []
        for line in lines[1:]:
            x, y, z = support.parse_numbers_comma(line)
            points.append((x, y, z))
        return cls(int(sid_s), points)


class AxisInfo(NamedTuple):
    axis: int
    sign: int
    diff: int


def x_edges_from(
        src: Scanner,
        scanners_by_id: dict[int, Scanner],
) -> dict[int, AxisInfo]:
    x_edges = {}
    for other in scanners_by_id.values():
        for axis in (0, 1, 2):
            for sign in (-1, 1):
                d_x: collections.Counter[int] = collections.Counter()
                for x, _, _ in src.points:
                    for other_pt in other.points:
                        d_x[x - other_pt[axis] * sign] += 1

                (x_diff, n), = d_x.most_common(1)
                if n >= 12:
                    x_edges[other.sid] = AxisInfo(
                        axis=axis,
                        sign=sign,
                        diff=x_diff,
                    )
    return x_edges


def yz_edges_from(
        src: Scanner,
        x_edges: dict[int, AxisInfo],
        scanners_by_id: dict[int, Scanner],
) -> tuple[dict[int, AxisInfo], dict[int, AxisInfo]]:
    y_edges = {}
    z_edges = {}

    for dst_id in x_edges:
        other = scanners_by_id[dst_id]
        for axis in (0, 1, 2):
            for sign in (-1, 1):
                d_y: collections.Counter[int] = collections.Counter()
                d_z: collections.Counter[int] = collections.Counter()
                for _, y, z in src.points:
                    for other_pt in other.points:
                        d_y[y - other_pt[axis] * sign] += 1
                        d_z[z - other_pt[axis] * sign] += 1

                (y_diff, y_n), = d_y.most_common(1)
                if y_n >= 12:
                    y_edges[dst_id] = AxisInfo(
                        axis=axis,
                        sign=sign,
                        diff=y_diff,
                    )

                (z_diff, z_n), = d_z.most_common(1)
                if z_n >= 12:
                    z_edges[dst_id] = AxisInfo(
                        axis=axis,
                        sign=sign,
                        diff=z_diff,
                    )

    return y_edges, z_edges


def compute(s: str) -> int:
    scanners = [Scanner.from_str(part) for part in s.split('\n\n')]
    scanners_by_id = {scanner.sid: scanner for scanner in scanners}
    scanner_positions = {0: (0, 0, 0)}

    todo = [scanners_by_id.pop(0)]
    while todo:
        src = todo.pop()

        x_edges = x_edges_from(src, scanners_by_id)
        y_edges, z_edges = yz_edges_from(src, x_edges, scanners_by_id)

        for k in x_edges:
            dst_x = x_edges[k].diff
            dst_y = y_edges[k].diff
            dst_z = z_edges[k].diff

            scanner_positions[k] = (dst_x, dst_y, dst_z)

            next_scanner = scanners_by_id.pop(k)
            next_scanner.points[:] = [
                (
                    dst_x + x_edges[k].sign * pt[x_edges[k].axis],
                    dst_y + y_edges[k].sign * pt[y_edges[k].axis],
                    dst_z + z_edges[k].sign * pt[z_edges[k].axis],
                )
                for pt in next_scanner.points
            ]

            todo.append(next_scanner)

    max_dist = 0
    positions = list(scanner_positions.values())
    for i, (x1, y1, z1) in enumerate(positions):
        for x2, y2, z2 in positions[i:]:
            max_dist = max(
                abs(x2 - x1) + abs(y2 - y1) + abs(z2 - z1),
                max_dist,
            )

    return max_dist


INPUT_S = '''\
--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14
'''
EXPECTED = 3621


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
