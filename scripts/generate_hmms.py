#!/usr/bin/env python

import argparse
import sys
from pathlib import Path

import pyhmmer


def create_hmm_from_msa(msa, alphabet, set_ga):
    builder = pyhmmer.plan7.Builder(alphabet)
    background = pyhmmer.plan7.Background(alphabet)
    hmm, _, _ = builder.build_msa(msa, background)
    hmm.command_line = None
    if set_ga:
        hmm.cutoffs.gathering = set_ga, set_ga
    return hmm


def generate_hmms(input_msas, input_format, set_ga):
    alphabet = pyhmmer.easel.Alphabet.amino()
    hmm_list = []
    for p in input_msas:
        with pyhmmer.easel.MSAFile(
            p, digital=True, alphabet=alphabet, format=input_format
        ) as fi:
            msa = fi.read()
            msa.name = p.stem.encode("utf-8")
            msa.accession = p.stem.encode("utf-8")
            hmm = create_hmm_from_msa(msa, alphabet, set_ga)
            hmm_list.append(hmm)
    return hmm_list


def write_hmms(hmms, output_hmm, write_ascii):
    binary = not write_ascii
    with open(output_hmm, "wb") as fo:
        for hmm in hmms:
            hmm.write(fo, binary=binary)


def main():
    parser = argparse.ArgumentParser(
        description="Generate HMMs from a set of multiple sequence alignments.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        allow_abbrev=False,
    )
    parser.add_argument("output_hmm", type=Path, help="Output HMM file.")
    parser.add_argument(
        "input_msas",
        type=Path,
        nargs="+",
        help="Input multiple sequence alignment file(s).",
    )
    parser.add_argument(
        "--set-ga",
        type=float,
        default=None,
        help="Set the gathering cutoff for the resulting HMMs.",
    )
    parser.add_argument(
        "--ascii-hmm",
        action="store_true",
        help="Output ASCII HMM instead of the binary format.",
    )
    parser.add_argument(
        "--input-format",
        type=str,
        default="afa",
        help="Format of the input MSAs.",
        choices=[
            "a2m",
            "afa",
            "clustal",
            "clustallike",
            "daemon",
            "ddbj",
            "embl",
            "fasta",
            "fmindex",
            "genbank",
            "hmmpgmd",
            "ncbi",
            "pfam",
            "phylip",
            "phylips",
            "psiblast",
            "selex",
            "stockholm",
            "uniprot",
        ],
    )

    # Print help if no arguments are provided
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    hmms = generate_hmms(args.input_msas, args.input_format, args.set_ga)
    write_hmms(hmms, args.output_hmm, args.ascii_hmm)


if __name__ == "__main__":
    main()
