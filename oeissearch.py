# search offline dumps of the On-Line Encyclopedia of Integer Sequences;
# requires the files "names" and "stripped" from
# https://oeis.org/wiki/QandA_For_New_OEIS#The_files_stripped.gz.2C_names.gz

import argparse, itertools, os, re, sys

# regexes for validating command line arguments and OEIS files
REGEX_SEQNUM = re.compile(  # sequence number or nothing
    r"^( A[0-9]{6} )?$", re.VERBOSE | re.IGNORECASE
)
REGEX_SEQNUM_PREFIX = re.compile(  # prefix of sequence number
    r"^( A[0-9]{0,6} )?$", re.VERBOSE | re.IGNORECASE
)
REGEX_INTEGER_LIST = re.compile(  # zero or more integers separated by commas
    r"^( -?[0-9]+ ( ,-?[0-9]+ )* )?$", re.VERBOSE | re.IGNORECASE
)
REGEX_NAMES_LINE = re.compile(  # non-comment line in names file
    r"^(A[0-9]{6}) (.+)$", re.IGNORECASE
)
REGEX_TERMS_LINE = re.compile(  # non-comment line in terms file
    r"^(A[0-9]{6}) (,(-?[0-9]+,)+)$", re.IGNORECASE
)

def parse_args():
    # parse command line arguments using argparse

    parser = argparse.ArgumentParser(
        description="Search offline dumps of the OEIS. All arguments are "
        "optional and, except for --type and --output, case insensitive. An "
        "OEIS sequence number (id) is an 'A' followed by six digits."
    )

    parser.add_argument(
        "-y", "--type", choices=("a", "nd", "y"), default="y",
        help="Find sequences whose terms are in ascending order (a), "
        "nondescending order (nd) or any order (y, default)."
    )
    parser.add_argument(
        "-d", "--description", type=str, default="",
        help="Find string in sequence descriptions case-insensitively."
    )
    parser.add_argument(
        "-n", "--seqnum", type=str, default="",
        help="Find by prefix of sequence number. 'A' followed by 0-6 digits. "
        "Default: none."
    )
    parser.add_argument(
        "-t", "--terms", type=str, default="",
        help="Find sequences that contain all of these terms, in *any* order, "
        "possibly with other terms in between. A comma-separated list of "
        "integers."
    )
    parser.add_argument(
        "-c", "--conseqterms", type=str, default="",
        help="Find sequences that contain all of these terms, in the "
        "*specified* order, with *no* other terms in between. A "
        "comma-separated list of integers."
    )
    parser.add_argument(
        "-o", "--output", choices=("m", "s"), default="m",
        help="Output format of each sequence. m = multiline (default), "
        "s = single line."
    )
    parser.add_argument(
        "--namesfile", type=str, default="names",
        help="The file with descriptions of OEIS sequences. Default: 'names'."
    )
    parser.add_argument(
        "--termsfile", type=str, default="stripped",
        help="The file with terms of OEIS sequences. Default: 'stripped'."
    )

    parser.add_argument(
        "-b", "--subseq", type=str, default="",
        help="Find subsequences. An OEIS sequence number (e.g. A000040). "
        "*To be implemented*"
    )
    parser.add_argument(
        "-p", "--superseq", type=str, default="",
        help="Find supersequences. An OEIS sequence number (e.g. A000040). "
        "*To be implemented*"
    )

    args = parser.parse_args()

    if REGEX_SEQNUM.search(args.subseq) is None:
        sys.exit("Value of --subseq argument is not valid.")
    if REGEX_SEQNUM.search(args.superseq) is None:
        sys.exit("Value of --superseq argument is not valid.")
    if REGEX_SEQNUM_PREFIX.search(args.seqnum) is None:
        sys.exit("Value of --seqnum syntax is not valid.")

    if REGEX_INTEGER_LIST.search(args.terms) is None:
        sys.exit("Value of --terms syntax is not valid.")
    if REGEX_INTEGER_LIST.search(args.conseqterms) is None:
        sys.exit("Value of --conseqterms argument is not valid.")

    if not os.path.isfile(args.namesfile):
        sys.exit(f"--namesfile '{args.namesfile}' not found.")
    if not os.path.isfile(args.termsfile):
        sys.exit(f"--termsfile '{args.termsfile}' not found.")

    return args

def parse_names_file(filename):
    # parse OEIS names file; syntax:
    #     # comment
    #     A000000 description
    # generate: (sequence_number, description)

    with open(filename, "rt") as handle:
        handle.seek(0)
        for line in handle:
            if not line.startswith("#"):
                line = line.rstrip("\n")
                match = REGEX_NAMES_LINE.search(line)
                if match is None:
                    sys.exit("Syntax error in names file: " + line)
                yield match.groups()

def parse_terms_file(filename):
    # parse OEIS terms file; syntax:
    #     # comment
    #     A000000 ,1,2,3,4,5
    # generate: (sequence_number, tuple_of_terms)

    with open(filename, "rt") as handle:
        handle.seek(0)
        for line in handle:
            if not line.startswith("#"):
                line = line.rstrip("\n")
                match = REGEX_TERMS_LINE.search(line)
                if match is None:
                    sys.exit("Syntax error in terms file: " + line)
                yield (
                    match.group(1),
                    tuple(int(n) for n in match.group(2).split(",") if n)
                )

def parse_int_list(stri):
    # parse a comma-separated list of integers from args
    if not stri:
        return tuple()
    return tuple(int(i) for i in stri.split(","))

def is_slice_of(needle, haystack):
    # is iterable (e.g. tuple) a slice of another iterable (e.g. tuple);
    # e.g. is_slice_of([2,3], [1,2,3,4]) = True
    return not needle or any(
        needle == haystack[s:e]
        for (s, e) in itertools.combinations(range(len(haystack) + 1), 2)
    )

def is_seq_ascending(seq):
    # is each term greater than the preceding one?
    return all(b > a for (a, b) in zip(seq, seq[1:]))

def is_seq_nondescending(seq):
    # is each term greater than or equal to the preceding one?
    return all(b >= a for (a, b) in zip(seq, seq[1:]))

def main():
    args = parse_args()

    # which sequence numbers to get from names file
    descriptionsBySeq = dict(
        (seq, descr) for (seq, descr) in parse_names_file(args.namesfile)
        if seq.startswith(args.seqnum.upper())
        and args.description.lower() in descr.lower()
    )

    # which sequence numbers to get from terms file
    argTermsParsed = parse_int_list(args.terms)
    argConseqTermsParsed = parse_int_list(args.conseqterms)
    termsBySeq = dict(
        (seq, terms) for (seq, terms) in parse_terms_file(args.termsfile)
        if seq.startswith(args.seqnum.upper())
        and all(t in terms for t in argTermsParsed)
        and is_slice_of(argConseqTermsParsed, terms)
        and (args.type != "a"  or is_seq_ascending(terms))
        and (args.type != "nd" or is_seq_nondescending(terms))
    )

    resultSeqs = sorted(set(descriptionsBySeq) & set(termsBySeq))

    if args.output == "s":
        for seq in resultSeqs:
            print(
                seq
                + " " + descriptionsBySeq[seq]
                + " " + ", ".join(str(t) for t in termsBySeq[seq])
            )
    else:
        for seq in resultSeqs:
            print(seq + " " + descriptionsBySeq[seq])
            print(", ".join(str(t) for t in termsBySeq[seq]))
            print()

main()
