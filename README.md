# oeis-search
A command-line Python program that searches offline dumps of the [On-Line Encyclopedia of Integer Sequences](https://oeis.org) (OEIS) and prints sequences that match *all* specified criteria.

Table of contents:
* [Requirements](#requirements)
* [Command line arguments](#command-line-arguments)
* [Example 1](#example-1)
* [Example 2](#example-2)

## Requirements
Requires the files `names` and `stripped` from [here](https://oeis.org/wiki/QandA_For_New_OEIS#The_files_stripped.gz.2C_names.gz). Download `names.gz` and `stripped.gz` and uncompress them in the same directory as this program. (Use `gunzip` on Linux or 7-Zip on Windows to uncompress.)

## Command line arguments
All arguments are optional.

### How to search the names file
Tip: to speed up the search, specify at least one of these options.
* `--minanum INTEGER`: Find sequences whose A-number is greater than or equal to `INTEGER`. `INTEGER` must be 0 or greater. The default is 0.
* `--maxanum INTEGER`: Find sequences whose A-number is less than or equal to `INTEGER`. `INTEGER` must be greater than or equal to `--minanum`. The default is 999999.
* `--descr TEXT`: Find sequences whose description contains `TEXT` case-insensitively.

### How to search the terms file
* `--searchfirst INTEGER`: When searching, only consider `INTEGER` first terms in each sequence. (The rest are ignored.) `INTEGER` must be 0 or greater. 0 means all terms are searched. The default is 0. This option affects all other options in this section.
* `--terms LIST`: Find sequences that contain all terms specified by `LIST`, in *any* order, possibly *with* other terms in between. `LIST` is a comma-separated list of integers, e.g. `"1,2,3"`.
* `--consec LIST`: Find sequences that contain all terms specified by `LIST`, in the *specified* order, with *no* other terms in between. `LIST` is a comma-separated list of integers, e.g. `"1,2,3"`.
* `--noterms LIST`: Find sequences that do *not* contain any term specified by `LIST`. `LIST` is a comma-separated list of integers, e.g. `"1,2,3"`.
* `--minmin INTEGER`: Find sequences whose *smallest* term is `INTEGER` or *greater*.
* `--minmax INTEGER`: Find sequences whose *smallest* term is `INTEGER` or *smaller*.
* `--maxmin INTEGER`: Find sequences whose *greatest* term is `INTEGER` or *greater*.
* `--maxmax INTEGER`: Find sequences whose *greatest* term is `INTEGER` or *smaller*.
* `--termorder ORDER`: Find sequences whose terms are in `ORDER`. `ORDER` is one of the following:
  * `a` = (non-strictly) ascending (e.g. 1, 1, 2, &hellip;)
  * `d` = (non-strictly) descending (e.g. 2, 2, 1, &hellip;)
  * `n` = neither ascending or descending (e.g. 1, 2, 1, &hellip;)
  * `y` = any (the default).
* `--distinct DISTINCT`: Find sequences with distinct values? `DISTINCT` is one of the following:
  * `y` = yes (find sequences whose values are all distinct)
  * `n` = no (find sequences containing at least some duplicate values)
  * `a` = any (the default)

### How to output the results
* `--sort ORDER`: Print results in `ORDER`. `ORDER` is one of the following:
  * `a` = by A-number (the default)
  * `d` = by description
  * `t` = by terms.
* `--format FORMAT`: Print information about each sequence in `FORMAT`. `FORMAT` is one of the following:
  * `m` = A-number, description and terms on multiple lines (the default)
  * `adt` = A-number, description and terms on a single line
  * `ad` = A-number and description on a single line
  * `at` = A-number and terms on a single line
  * `a` = A-number on a single line.
* `--printfirst INTEGER`: Do not print more than `INTEGER` first terms of each sequence. `INTEGER` must be 0 or greater. 0 means all terms are printed. The default is 0.

### Miscellaneous options
* `--namefile FILE`: Read A-numbers and names of sequences from `FILE`. Default: `names`.
* `--termfile FILE`: Read A-numbers and terms of sequences from `FILE`. Default: `stripped`.
* `--quiet`: Do not print status messages ("reading file..." etc.).
* `-h` or `--help`: print a short summary of these command line arguments and exit.

## Example 1
```
$ python3 oeissearch.py --descr "prime" --terms "1,4,5,9,64" --termorder a \
--distinct y --sort d
Searching 'names'...
Searching 'stripped'...
Found 256 sequence(s).

A051038: 11-smooth numbers: numbers whose prime divisors are all <= 11.
1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25, 27,
28, 30, 32, 33, 35, 36, 40, 42, 44, 45, 48, 49, 50, 54, 55, 56, 60, 63, 64, 66,
70, 72, 75, 77, 80, 81, 84, 88, 90, 96, 98, 99, 100, 105, 108, 110, 112, 120,
121, 125, 126, 128, 132, 135, 140

A080197: 13-smooth numbers: numbers whose prime divisors are all <= 13.
1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 20, 21, 22, 24, 25,
26, 27, 28, 30, 32, 33, 35, 36, 39, 40, 42, 44, 45, 48, 49, 50, 52, 54, 55, 56,
60, 63, 64, 65, 66, 70, 72, 75, 77, 78, 80, 81, 84, 88, 90, 91, 96, 98, 99,
100, 104, 105, 108, 110, 112, 117, 120

(snip)
```

## Example 2
```
$ python3 oeissearch.py --consec 19,84 --maxmax 200 --format ad --quiet
A065266: A065264 conjugated with A059893, inverse of A065265.
A065290: A065288 conjugated with A059893, inverse of A065289.
A173823: a(n) shows the digit sum of a(n+1) + a(n+2).
A191514: Lehrer's elementary sequence.
A294886: Sum of deficient proper divisors of n.
A340587: a(n) is the least root of A340586(n).
```
