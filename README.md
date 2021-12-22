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
+ python day11/part1.py day11/input.txt
1637
> 19016 μs
+ python day11/part2.py day11/input.txt
242
> 43382 μs
+ python day12/part1.py day12/input.txt
4573
> 27702 μs
+ python day12/part2.py day12/input.txt
117509
> 810 ms
+ python day13/part1.py day13/input.txt
807
> 1397 μs
+ python day13/part2.py day13/input.txt
#     ##  #  # ####  ##  #  # ####   ##
#    #  # #  # #    #  # #  # #       #
#    #    #### ###  #    #  # ###     #
#    # ## #  # #    # ## #  # #       #
#    #  # #  # #    #  # #  # #    #  #
####  ### #  # ####  ###  ##  ####  ##
> 2839 μs
+ python day14/part1.py day14/input.txt
3095
> 12231 μs
+ python day14/part2.py day14/input.txt
3152788426516
> 6875 μs
+ python day15/part1.py day15/input.txt
621
> 99360 μs
+ python day15/part2.py day15/input.txt
2904
> 3904 ms
+ python day16/part1.py day16/input.txt
906
> 2082 μs
+ python day16/part2.py day16/input.txt
819324480368
> 2146 μs
+ python day17/part1.py day17/input.txt
8646
> 31 μs
+ python day17/part2.py day17/input.txt
5945
> 432 ms
+ python day18/part1.py day18/input.txt
4017
> 253 ms
+ python day18/part2.py day18/input.txt
4583
> 4660 ms
+ python day19/part1.py day19/input.txt
381
> 1419 ms
+ python day19/part2.py day19/input.txt
12201
> 1424 ms
+ python day20/part1.py day20/input.txt
5437
> 155 ms
+ python day20/part2.py day20/input.txt
19340
> 8706 ms
+ python day21/part1.py day21/input.txt
989352
> 912 μs
+ python day21/part2.py day21/input.txt
430229563871565
> 104 ms
+ python day22/part1.py day22/input.txt
583641
> 1380 ms
```
