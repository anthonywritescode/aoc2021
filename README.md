[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/anthonywritescode/aoc2021/main.svg)](https://results.pre-commit.ci/latest/github/anthonywritescode/aoc2021/main)

advent of code 2021
===================

https://adventofcode.com/2021

### stream / youtube

- [Streamed daily on twitch](https://twitch.tv/anthonywritescode)
- [Streams uploaded to youtube afterwards](https://www.youtube.com/channel/UChPxcypesw8L-iqltstSI4Q)
- [Uploaded to youtube afterwards](https://www.youtube.com/anthonywritescode)

### about

for 2021, I'm planning to implement in python and then some meme language...
maybe.

### timing

- comparing to these numbers isn't necessarily useful
- normalize your timing to day 1 part 1 and compare
- alternate implementations are listed in parens
- these timings are very non-scientific (sample size 1)

```console
$ find -maxdepth 1 -type d -name 'day*' -not -name day00 | sort | xargs --replace bash -xc 'python {}/part1.py {}/input.txt; python {}/part2.py {}/input.txt'
+ python day01/part1.py day01/input.txt
1195
> 1208 μs
+ python day01/part2.py day01/input.txt
1235
> 1196 μs
+ python day02/part1.py day02/input.txt
1947824
> 675 μs
+ python day02/part2.py day02/input.txt
1813062561
> 736 μs
+ python day03/part1.py day03/input.txt
3277364
> 2797 μs
+ python day03/part2.py day03/input.txt
5736383
> 7091 μs (haxy dicts)
5736383
> 2184 μs
+ python day04/part1.py day04/input.txt
60368
> 17870 μs
+ python day04/part2.py day04/input.txt
17435
> 44811 μs
+ python day05/part1.py day05/input.txt
5197
> 142 ms
+ python day05/part2.py day05/input.txt
18605
> 261 ms
+ python day06/part1.py day06/input.txt
383160
> 922 μs
+ python day06/part2.py day06/input.txt
1721148811504
> 2567 μs
+ python day07/part1.py day07/input.txt
335330
> 711 μs
+ python day07/part2.py day07/input.txt
92439766
> 3680 μs
+ python day08/part1.py day08/input.txt
519
> 472 μs
+ python day08/part2.py day08/input.txt
1027483
> 10599 μs
+ python day09/part1.py day09/input.txt
506
> 12520 μs
+ python day09/part2.py day09/input.txt
931200
> 46183 μs
+ python day10/part1.py day10/input.txt
316851
> 2531 μs
+ python day10/part2.py day10/input.txt
2182912364
> 2763 μs
```
