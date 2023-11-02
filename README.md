# oeis-search
Search offline dumps of the On-Line Encyclopedia of Integer Sequences (OEIS).

Requires the files `names` and `stripped` from [here](https://oeis.org/wiki/QandA_For_New_OEIS#The_files_stripped.gz.2C_names.gz).

Note that the `--subseq` and `--superseq` options haven't been implemented yet.

## Help text
```
usage: oeissearch.py [-h] [-y {a,nd,y}] [-d DESCRIPTION] [-n SEQNUM]
                     [-t TERMS] [-c CONSEQTERMS] [-o {m,s}]
                     [--namesfile NAMESFILE] [--termsfile TERMSFILE]
                     [-b SUBSEQ] [-p SUPERSEQ]

Search offline dumps of the OEIS. All arguments are optional and, except for
--type and --output, case insensitive. An OEIS sequence number (id) is an 'A'
followed by six digits.

options:
  -h, --help            show this help message and exit
  -y {a,nd,y}, --type {a,nd,y}
                        Find sequences whose terms are in ascending order (a),
                        nondescending order (nd) or any order (y, default).
  -d DESCRIPTION, --description DESCRIPTION
                        Find string in sequence descriptions case-
                        insensitively.
  -n SEQNUM, --seqnum SEQNUM
                        Find by prefix of sequence number. 'A' followed by 0-6
                        digits. Default: none.
  -t TERMS, --terms TERMS
                        Find sequences that contain all of these terms, in
                        *any* order, possibly with other terms in between. A
                        comma-separated list of integers.
  -c CONSEQTERMS, --conseqterms CONSEQTERMS
                        Find sequences that contain all of these terms, in the
                        *specified* order, with *no* other terms in between. A
                        comma-separated list of integers.
  -o {m,s}, --output {m,s}
                        Output format of each sequence. m = multiline
                        (default), s = single line.
  --namesfile NAMESFILE
                        The file with descriptions of OEIS sequences. Default:
                        'names'.
  --termsfile TERMSFILE
                        The file with terms of OEIS sequences. Default:
                        'stripped'.
  -b SUBSEQ, --subseq SUBSEQ
                        Find subsequences. An OEIS sequence number (e.g.
                        A000040). *To be implemented*
  -p SUPERSEQ, --superseq SUPERSEQ
                        Find supersequences. An OEIS sequence number (e.g.
                        A000040). *To be implemented*
```

## Example
```
$ python3 oeissearch.py -y a -d "prime" -n "A0000" -t "3,17"

A000028 Let n = p_1^e_1 p_2^e_2 p_3^e_3 ... be the prime factorization of n.
Sequence gives n such that the sum of the numbers of 1's in the binary
expansions of e_1, e_2, e_3, ... is odd.
2, 3, 4, 5, 7, 9, 11, 13, 16, 17, 19, 23, 24, 25, 29, 30, 31, 37, 40, 41, 42,
43, 47, 49, 53, 54, 56, 59, 60, 61, 66, 67, 70, 71, 72, 73, 78, 79, 81, 83, 84,
88, 89, 90, 96, 97, 101, 102, 103, 104, 105, 107, 108, 109, 110, 113, 114, 121,
126, 127, 128, 130, 131, 132, 135, 136, 137

A000040 The prime numbers.
2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73,
79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157,
163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241,
251, 257, 263, 269, 271

(snip)
```
