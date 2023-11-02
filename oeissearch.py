# search offline dumps of the On-Line Encyclopedia of Integer Sequences;
# requires the files "names" and "stripped" from
# https://oeis.org/wiki/QandA_For_New_OEIS#The_files_stripped.gz.2C_names.gz

import argparse, itertools, os, re, sys

# regexes for validating command line arguments
REGEX_ANUM = re.compile(  # A-number or nothing
    r"^( A[0-9]{6} )?$", re.VERBOSE | re.IGNORECASE
)
REGEX_ANUM_PREFIX = re.compile(  # prefix of an A-number
    r"^( A[0-9]{0,6} )?$", re.VERBOSE | re.IGNORECASE
)
REGEX_INTEGER_LIST = re.compile(  # zero or more integers separated by commas
    r"^( -?[0-9]+ ( ,-?[0-9]+ )* )?$", re.VERBOSE | re.IGNORECASE
)

# regexes for validating OEIS files
REGEX_NAMES_LINE = re.compile(  # non-comment line in names file
    r"^(A[0-9]{6})\ (.+)$", re.VERBOSE | re.IGNORECASE
)
REGEX_TERMS_LINE = re.compile(  # non-comment line in terms file
    r"^(A[0-9]{6})\ ,( -?[0-9]+ (,-?[0-9]+)* ),$", re.VERBOSE | re.IGNORECASE
)

def parse_args():
    # parse command line arguments using argparse

    parser = argparse.ArgumentParser(
        description="Search offline dumps of the OEIS for sequences that "
        "match all specified criteria. All arguments are optional. All "
        "arguments except --type, --sort and --format are case insensitive."
    )

    # search
    parser.add_argument(
        "-d", "--description", type=str, default="",
        help="Find this text in sequence descriptions, e.g. 'prime'."
    )
    parser.add_argument(
        "-t", "--terms", type=str, default="",
        help="Find sequences that contain all these terms, in any order, "
        "possibly with other terms in between. A comma-separated list of "
        "integers, e.g. '1,2,3'."
    )
    parser.add_argument(
        "-c", "--conseqterms", type=str, default="",
        help="Find sequences that contain all these terms, in the specified "
        "order, with no other terms in between. A comma-separated list of "
        "integers, e.g. '1,2,3'."
    )
    parser.add_argument(
        "-n", "--noterms", type=str, default="",
        help="Find sequences that do not contain any of these terms. A "
        "comma-separated list of integers, e.g. '1,2,3'."
    )
    parser.add_argument(
        "-b", "--subseq", type=str, default="",
        help="Find subsequences of this A-number (e.g. 'A000040'). Note: for "
        "each sequence, terms greater than the greatest term in this sequence "
        "are ignored. E.g. 2,4,6 is considered a subsequence of 1,2,3,4,5."
    )
    parser.add_argument(
        "-p", "--superseq", type=str, default="",
        help="Find supersequences of this A-number (e.g. 'A000040'). Note: "
        "terms greater than max(s) in this sequence are ignored for each "
        "sequence s. E.g. 1,2,3,4,5 is considered a supersequence of 2,4,6."
    )
    parser.add_argument(
        "-y", "--type", choices=("a", "nd", "y"), default="y",
        help="Find sequences with their terms in this order: 'a' = strictly "
        "ascending, 'nd' = nondescending, 'y' = any (default)."
    )
    parser.add_argument(
        "-a", "--anum", type=str, default="",
        help="Find by A-number prefix ('A' followed by 0-6 digits). E.g. "
        "'A000' will find sequences A000000-A000999."
    )

    # output
    parser.add_argument(
        "-s", "--sort", choices=("a", "d", "t"), default="a",
        help="Print results in this order: 'a' = by A-number (default), 'd' = "
        "by description, 't' = by terms."
    )
    parser.add_argument(
        "-f", "--format", choices=("m", "adt", "ad", "at", "a"), default="m",
        help="How to print each sequence: 'm' = A-number & description & "
        "terms on multiple lines (default), 'adt' = A-number & description & "
        "terms, 'ad' = A-number & description, 'at' = A-number & terms, 'a' = "
        "A-number."
    )
    parser.add_argument(
        "--maxterms", type=int, default=0,
        help="Do not print more than this many first terms of each sequence. "
        "A nonnegative integer. 0 = unlimited (default)."
    )
    parser.add_argument(
        "--quiet", action="store_true",
        help="Do not print status messages ('reading file...' etc.)."
    )

    # other
    parser.add_argument(
        "--namesfile", type=str, default="names",
        help="File to read descriptions of sequences from. Default: 'names'."
    )
    parser.add_argument(
        "--termsfile", type=str, default="stripped",
        help="File to read terms of sequences from. Default: 'stripped'."
    )

    args = parser.parse_args()

    # search
    if REGEX_INTEGER_LIST.search(args.terms) is None:
        sys.exit("Value of --terms argument is not valid.")
    if REGEX_INTEGER_LIST.search(args.conseqterms) is None:
        sys.exit("Value of --conseqterms argument is not valid.")
    if REGEX_INTEGER_LIST.search(args.noterms) is None:
        sys.exit("Value of --noterms argument is not valid.")
    if REGEX_ANUM.search(args.subseq) is None:
        sys.exit("Value of --subseq argument is not valid.")
    if REGEX_ANUM.search(args.superseq) is None:
        sys.exit("Value of --superseq argument is not valid.")
    if REGEX_ANUM_PREFIX.search(args.anum) is None:
        sys.exit("Value of --anum argument is not valid.")

    # output
    if args.maxterms < 0:
        sys.exit("Value of --maxterms argument is not valid.")

    # other
    if not os.path.isfile(args.namesfile):
        sys.exit(f"--namesfile '{args.namesfile}' not found.")
    if not os.path.isfile(args.termsfile):
        sys.exit(f"--termsfile '{args.termsfile}' not found.")

    return args

def parse_names_file(filename):
    # parse OEIS names file; syntax:
    #     # comment
    #     A000000 description
    # generate: (a_number, description)

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
    #     A000000 ,1,2,3,
    # generate: ("A000000", "1,2,3")

    with open(filename, "rt") as handle:
        handle.seek(0)
        for line in handle:
            if not line.startswith("#"):
                line = line.rstrip("\n")
                match = REGEX_TERMS_LINE.search(line)
                if match is None:
                    sys.exit("Syntax error in terms file: " + line)
                # don't split the terms here (slow and not always needed)
                yield match.group(1, 2)

def parse_int_list(stri):
    # parse a comma-separated list of integers from args
    if not stri:
        return tuple()
    return tuple(int(i) for i in stri.split(","))

def get_seq_terms(seqToFind, termsFile):
    # get terms of specified sequence as a set (seq is from args)

    seqToFind = seqToFind.upper()
    print(f"Getting info on {seqToFind} from '{termsFile}'...")
    termsFound = None
    for (seq, terms) in parse_terms_file(termsFile):
        if seq == seqToFind:
            return set(int(n) for n in terms.split(","))
    sys.exit(f"{seqToFind} not found in '{termsFile}'.")

def is_slice_of(needle, haystack):
    # is iterable (e.g. tuple) a slice of another iterable (e.g. tuple)?
    # e.g. is_slice_of([2,3], [1,2,3,4]) = True
    return not needle or (
        set(needle).issubset(set(haystack))  # speed optimization
        and any(
            needle == haystack[s:e]
            for (s, e) in itertools.combinations(range(len(haystack) + 1), 2)
        )
    )

def is_seq_ascending(seq):
    # is each term greater than the preceding one?
    return all(b > a for (a, b) in zip(seq, seq[1:]))

def is_seq_nondescending(seq):
    # is each term greater than or equal to the preceding one?
    return all(b >= a for (a, b) in zip(seq, seq[1:]))

def is_subset(set1, set2):
    # does each term of set1 also occur in set2?
    # ignore terms in set1 greater than max(set2);
    # e.g. is_subset({2,4,6}, {1,2,3,4,5}) = True
    set2Max = max(set2)
    return set(t for t in set1 if t <= set2Max).issubset(set2)

def main():
    args = parse_args()

    # get matches (A-numbers) in names file
    if not args.quiet:
        print(f"Searching '{args.namesfile}'...")
    nameResults = set()
    for (seq, descr) in parse_names_file(args.namesfile):
        if (
            seq.startswith(args.anum.upper())
            and args.description.lower() in descr.lower()
        ):
            nameResults.add(seq)

    argTermsParsed = parse_int_list(args.terms)
    argConseqTermsParsed = parse_int_list(args.conseqterms)
    argNoTermsParsed = parse_int_list(args.noterms)
    if args.subseq:
        subsetOf = get_seq_terms(args.subseq, args.termsfile)
    if args.superseq:
        supersetOf = get_seq_terms(args.superseq, args.termsfile)

    # get final results from nameResults and the terms file
    if not args.quiet:
        print(f"Searching '{args.termsfile}'...")
    finalResults = {}
    for (seq, terms) in parse_terms_file(args.termsfile):
        if seq in nameResults:
            terms = tuple(int(n) for n in terms.split(","))
            if (
                all(t in terms for t in argTermsParsed)
                and is_slice_of(argConseqTermsParsed, terms)
                and not any(t in terms for t in argNoTermsParsed)
                and (args.type != "a"  or is_seq_ascending(terms))
                and (args.type != "nd" or is_seq_nondescending(terms))
                and (args.subseq   == "" or is_subset(set(terms), subsetOf))
                and (args.superseq == "" or is_subset(supersetOf, set(terms)))
            ):
                finalResults[seq] = ("???", terms)  # description added later
    del nameResults

    # get descriptions of final results
    for (seq, descr) in parse_names_file(args.namesfile):
        if seq in finalResults:
            finalResults[seq] = (descr, finalResults[seq][1])

    # sort results
    if args.sort == "a":
        sortedResults = sorted(finalResults)
    elif args.sort == "d":
        sortedResults = sorted(finalResults, key=lambda s: finalResults[s][0])
        sortedResults.sort(key=lambda s: finalResults[s][0].lower())
    elif args.sort == "t":
        sortedResults = sorted(finalResults, key=lambda s: finalResults[s][1])
    else:
        sys.exit("Unexpected error.")

    if not args.quiet:
        print()

    # print results
    for seq in sortedResults:
        (descr, terms) = finalResults[seq]
        if args.maxterms:
            terms = terms[:args.maxterms]
        terms = ", ".join(str(t) for t in terms)

        if args.format == "m":
            print(f"{seq}:", descr)
            print(terms)
            print()
        elif args.format == "adt":
            print(f"{seq}:", descr, terms)
        elif args.format == "ad":
            print(f"{seq}:", descr)
        elif args.format == "at":
            print(f"{seq}:", terms)
        elif args.format == "a":
            print(seq)
        else:
            sys.exit("Unexpected error.")

main()
