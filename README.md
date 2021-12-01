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
+ python day01/part1.py input.txt
1195
> 1208 μs
+ python day01/part2.py input.txt
1235
> 1196 μs
```
