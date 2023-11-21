# search offline dumps of the On-Line Encyclopedia of Integer Sequences;
# requires the files "names" and "stripped" from
# https://oeis.org/wiki/QandA_For_New_OEIS#The_files_stripped.gz.2C_names.gz

import argparse, os, re, sys

# regexes for validating command line arguments
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
        "match all specified criteria. See the file README.md for details."
    )

    # search - names file
    parser.add_argument(
        "--minanum", type=int, default=0,
        help="Minimum A-number."
    )
    parser.add_argument(
        "--maxanum", type=int, default=999999,
        help="Maximum A-number."
    )
    parser.add_argument(
        "--descr", type=str, default="",
        help="Text in sequence descriptions."
    )

    # search - terms file
    parser.add_argument(
        "--onlyfirst", type=int, default=0,
        help="Only consider this many first terms."
    )
    parser.add_argument(
        "--terms", type=str, default="",
        help="All these terms."
    )
    parser.add_argument(
        "--consec", type=str, default="",
        help="All these terms, in this order, without other terms in between."
    )
    parser.add_argument(
        "--noterms", type=str, default="",
        help="None of these terms."
    )
    parser.add_argument(
        "--lower", type=int, default=None,
        help="Smallest term is this or greater."
    )
    parser.add_argument(
        "--upper", type=int, default=None,
        help="Greatest term is this or smaller."
    )
    parser.add_argument(
        "--termorder", choices=("a", "d", "y"), default="y",
        help="Order of terms: 'a' = ascending, 'd' = descending, 'y' = any."
    )
    parser.add_argument(
        "--distinct", action="store_true",
        help="No duplicate terms."
    )

    # output
    parser.add_argument(
        "--sort", choices=("a", "d", "t"), default="a",
        help="Sort results by: 'a' = A-number, 'd' = description, 't' = terms."
    )
    parser.add_argument(
        "--format", choices=("m", "adt", "ad", "at", "a"), default="m",
        help="Print results as: 'm' = multiline, 'adt' = A-number & "
        "description & terms, 'ad' = A-number & description, 'at' = A-number "
        "& terms, 'a' = A-number."
    )
    parser.add_argument(
        "--maxprint", type=int, default=0,
        help="Only print this many first terms."
    )
    parser.add_argument(
        "--quiet", action="store_true",
        help="Don't print status messages."
    )

    # other
    parser.add_argument(
        "--namefile", type=str, default="names",
        help="File with sequence names."
    )
    parser.add_argument(
        "--termfile", type=str, default="stripped",
        help="File with sequence terms."
    )

    args = parser.parse_args()

    # search - names file
    if args.minanum < 0:
        sys.exit("Value of --minanum argument is not valid.")
    if args.maxanum < args.minanum:
        sys.exit("Value of --maxanum argument is not valid.")

    # search - terms file
    if args.onlyfirst < 0:
        sys.exit("Value of --onlyfirst argument is not valid.")
    if REGEX_INTEGER_LIST.search(args.terms) is None:
        sys.exit("Value of --terms argument is not valid.")
    if REGEX_INTEGER_LIST.search(args.consec) is None:
        sys.exit("Value of --consec argument is not valid.")
    if REGEX_INTEGER_LIST.search(args.noterms) is None:
        sys.exit("Value of --noterms argument is not valid.")

    # output
    if args.maxprint < 0:
        sys.exit("Value of --maxprint argument is not valid.")

    # other
    if not os.path.isfile(args.namefile):
        sys.exit(f"--namefile '{args.namefile}' not found.")
    if not os.path.isfile(args.termfile):
        sys.exit(f"--termfile '{args.termfile}' not found.")

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

def is_slice_of(needle, haystack):
    # is an iterable a slice of another iterable?
    return not needle or any(
        needle == haystack[i:i+len(needle)]
        for i in range(len(haystack) - len(needle) + 1)
    )

def is_seq_ascending(seq):
    # is each term greater than or equal to the preceding one?
    return all(b >= a for (a, b) in zip(seq, seq[1:]))

def is_seq_descending(seq):
    # is each term less than or equal to the preceding one?
    return all(b <= a for (a, b) in zip(seq, seq[1:]))

def main():
    args = parse_args()

    # get matches (A-numbers) in names file
    if not args.quiet:
        print(f"Searching '{args.namefile}'...")
    nameResults = set()
    for (seq, descr) in parse_names_file(args.namefile):
        if (
            args.minanum <= int(seq[1:]) <= args.maxanum
            and args.descr.lower() in descr.lower()
        ):
            nameResults.add(seq)

    argTermsParsed = parse_int_list(args.terms)
    argConsecParsed = parse_int_list(args.consec)
    argNoTermsParsed = parse_int_list(args.noterms)

    # get final results from nameResults and the terms file
    if not args.quiet:
        print(f"Searching '{args.termfile}'...")
    finalResults = {}
    for (seq, terms) in parse_terms_file(args.termfile):
        if seq in nameResults:
            allTerms = tuple(int(n) for n in terms.split(","))
            # terms to search
            terms = allTerms[:args.onlyfirst] if args.onlyfirst else allTerms
            if (
                all(t in terms for t in argTermsParsed)
                and is_slice_of(argConsecParsed, terms)
                and not any(t in terms for t in argNoTermsParsed)
                and (args.lower is None or min(terms) >= args.lower)
                and (args.upper is None or max(terms) <= args.upper)
                and (args.termorder != "a" or is_seq_ascending(terms))
                and (args.termorder != "d" or is_seq_descending(terms))
                and (not args.distinct or len(terms) == len(set(terms)))
            ):
                finalResults[seq] = ("???", allTerms) # description added later
    del nameResults

    if not args.quiet:
        print(f"Found {len(finalResults)} sequence(s).")

    # get descriptions of final results
    for (seq, descr) in parse_names_file(args.namefile):
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
        if args.maxprint:
            terms = terms[:args.maxprint]
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
