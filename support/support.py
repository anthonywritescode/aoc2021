from __future__ import annotations

import argparse
import contextlib
import time
import urllib.error
import urllib.request
from typing import Generator


@contextlib.contextmanager
def timing(name: str = '') -> Generator[None, None, None]:
    before = time.time()
    try:
        yield
    finally:
        after = time.time()
        t = (after - before) * 1000
        unit = 'ms'
        if t < 100:
            t *= 1000
            unit = 'μs'
        if name:
            name = f' ({name})'
        print(f'> {int(t)} {unit}{name}')


def get_input(year: int, day: int) -> str:
    with open('../.env') as f:
        contents = f.read()

    url = f'https://adventofcode.com/{year}/day/{day}/input'
    req = urllib.request.Request(url, headers={'Cookie': contents.strip()})
    return urllib.request.urlopen(req).read().decode()


def download_input() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('year', type=int)
    parser.add_argument('day', type=int)
    args = parser.parse_args()

    for i in range(5):
        try:
            s = get_input(args.year, args.day)
        except urllib.error.URLError as e:
            print(f'zzz: not ready yet: {e}')
            time.sleep(1)
        else:
            break
    else:
        raise SystemExit('timed out after attempting many times')

    with open('input.txt', 'w') as f:
        f.write(s)

    lines = s.splitlines()
    if len(lines) > 10:
        for line in lines[:10]:
            print(line)
        print('...')
    else:
        print(lines[0][:80])
        print('...')

    return 0
