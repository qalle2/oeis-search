# oeis-search
Search offline dumps of the On-Line Encyclopedia of Integer Sequences (OEIS).

Table of contents:
* [Requirements](#requirements)
* [Command line help text](#command-line-help-text)
* [Example](#example)

## Requirements
Requires the files `names` and `stripped` from [here](https://oeis.org/wiki/QandA_For_New_OEIS#The_files_stripped.gz.2C_names.gz).

## Command line help text
```
usage: oeissearch.py [-h] [-d DESCRIPTION] [-t TERMS] [-c CONSEQTERMS]
                     [-b SUBSEQ] [-p SUPERSEQ] [-y {a,nd,y}] [-a ANUM]
                     [-s {n,d,t}] [-f {m,ndt,nd,nt,n}] [--maxterms MAXTERMS]
                     [--quiet] [--namesfile NAMESFILE] [--termsfile TERMSFILE]

Search offline dumps of the OEIS for sequences that match all specified
criteria. All arguments are optional. All arguments except --type, --sort and
--format are case insensitive.

options:
  -h, --help            show this help message and exit
  -d DESCRIPTION, --description DESCRIPTION
                        Find this text in sequence descriptions, e.g. 'prime'.
  -t TERMS, --terms TERMS
                        Find sequences that contain all these terms, in any
                        order, possibly with other terms in between. A comma-
                        separated list of integers, e.g. '-1,2,3'.
  -c CONSEQTERMS, --conseqterms CONSEQTERMS
                        Find sequences that contain all these terms, in the
                        specified order, with no other terms in between. A
                        comma-separated list of integers, e.g. '-1,2,3'.
  -b SUBSEQ, --subseq SUBSEQ
                        Find subsequences of this A-number (e.g. 'A000040').
                        Note: for each sequence, terms greater than the
                        greatest term in this sequence are ignored. E.g. 2,4,6
                        is considered a subsequence of 1,2,3,4,5.
  -p SUPERSEQ, --superseq SUPERSEQ
                        Find supersequences of this A-number (e.g. 'A000040').
                        Note: terms greater than max(s) in this sequence are
                        ignored for each sequence s. E.g. 1,2,3,4,5 is
                        considered a supersequence of 2,4,6.
  -y {a,nd,y}, --type {a,nd,y}
                        Find sequences with their terms in this order: 'a' =
                        ascending, 'nd' = nondescending, 'y' = any (default).
  -a ANUM, --anum ANUM  Find by A-number prefix ('A' followed by 0-6 digits).
                        E.g. 'A000' will find sequences A000000-A000999.
  -s {n,d,t}, --sort {n,d,t}
                        Print results in this order: 'n' = by A-number
                        (default), 'd' = by description, 't' = by terms.
  -f {m,ndt,nd,nt,n}, --format {m,ndt,nd,nt,n}
                        How to print each sequence: 'm' = A-number &
                        description & terms on multiple lines (default), 'ndt'
                        = A-number & description & terms, 'nd' = A-number &
                        description, 'nt' = A-number & terms, 'n' = A-number.
  --maxterms MAXTERMS   Do not print more than this many first terms of each
                        sequence. A nonnegative integer. 0 = unlimited
                        (default).
  --quiet               Do not print status messages ('reading file...' etc.).
  --namesfile NAMESFILE
                        File to read descriptions of sequences from. Default:
                        'names'.
  --termsfile TERMSFILE
                        File to read terms of sequences from. Default:
                        'stripped'.
```

## Example
### Input
```
$ python3 oeissearch.py -d "prime" -t "1,4,5,9,64" -y a -s d
```

### Output
```
Searching 'names'...
Searching 'stripped'...

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
```
(snip)
