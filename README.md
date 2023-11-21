# oeis-search
Search offline dumps of the [On-Line Encyclopedia of Integer Sequences](https://oeis.org) (OEIS).

Table of contents:
* [Requirements](#requirements)
* [Command line help text](#command-line-help-text)
* [Example 1](#example-1)
* [Example 2](#example-2)

## Requirements
Requires the files `names` and `stripped` from [here](https://oeis.org/wiki/QandA_For_New_OEIS#The_files_stripped.gz.2C_names.gz).

## Command line help text
```
usage: oeissearch.py [-h] [--minanum MINANUM] [--maxanum MAXANUM]
                     [--descr DESCR] [--terms TERMS] [--consec CONSEC]
                     [--noterms NOTERMS] [--lower LOWER] [--upper UPPER]
                     [--termorder {a,d,y}] [--distinct]
                     [--onlyfirst ONLYFIRST] [--sort {a,d,t}]
                     [--format {m,adt,ad,at,a}] [--maxprint MAXPRINT]
                     [--quiet] [--namefile NAMEFILE] [--termfile TERMFILE]

Search offline dumps of the OEIS for sequences that match all specified
criteria. All arguments are optional. All arguments except --type, --sort and
--format are case insensitive.

options:
  -h, --help            show this help message and exit
  --minanum MINANUM     Minimum A-number. 0 or greater, default=0.
  --maxanum MAXANUM     Maximum A-number. Greater than or equal to --minanum,
                        default=999999.
  --descr DESCR         Find this text in sequence descriptions, e.g. 'prime'.
  --terms TERMS         Find sequences that contain all these terms, in any
                        order, possibly with other terms in between. A comma-
                        separated list of integers, e.g. '1,2,3'.
  --consec CONSEC       Find sequences that contain all these terms, in the
                        specified order, with no other terms in between. A
                        comma-separated list of integers, e.g. '1,2,3'.
  --noterms NOTERMS     Find sequences that do not contain any of these terms.
                        A comma-separated list of integers, e.g. '1,2,3'.
  --lower LOWER         Find sequences whose smallest term is this or greater.
                        An integer.
  --upper UPPER         Find sequences whose greatest term is this or smaller.
                        An integer.
  --termorder {a,d,y}   Find sequences with their terms in this order: 'a' =
                        (non-strictly) ascending, 'd' = (non-strictly)
                        descending, 'y' = any (default).
  --distinct            Only find sequences in which all terms are distinct.
  --onlyfirst ONLYFIRST
                        Only consider this many first terms in each sequence
                        when searching. (The rest are ignored.) 0 or greater.
                        Default=0 (all terms).
  --sort {a,d,t}        Print results in this order: 'a' = by A-number
                        (default), 'd' = by description, 't' = by terms.
  --format {m,adt,ad,at,a}
                        How to print each sequence: 'm' = A-number &
                        description & terms on multiple lines (default), 'adt'
                        = A-number & description & terms, 'ad' = A-number &
                        description, 'at' = A-number & terms, 'a' = A-number.
  --maxprint MAXPRINT   Do not print more than this many first terms of each
                        sequence. A nonnegative integer. 0 = unlimited
                        (default).
  --quiet               Do not print status messages ('reading file...' etc.).
  --namefile NAMEFILE   File to read descriptions of sequences from. Default:
                        'names'.
  --termfile TERMFILE   File to read terms of sequences from. Default:
                        'stripped'.
```

## Example 1
```
$ python3 oeissearch.py --descr "prime" --terms "1,4,5,9,64" --termorder a \
--distinct --sort d
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
$ python3 oeissearch.py --consec 19,84 --upper 200 --format ad --quiet
A065266: A065264 conjugated with A059893, inverse of A065265.
A065290: A065288 conjugated with A059893, inverse of A065289.
A173823: a(n) shows the digit sum of a(n+1) + a(n+2).
A191514: Lehrer's elementary sequence.
A294886: Sum of deficient proper divisors of n.
A340587: a(n) is the least root of A340586(n).
```
