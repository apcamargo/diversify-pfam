#!/usr/bin/env python

import argparse
import sys

from Bio import AlignIO
from Bio.Align import MultipleSeqAlignment
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord


def filter_uppercase_columns(alignment):
    # Get the number of sequences and the length of alignment
    alignment_length = alignment.get_alignment_length()
    # Find the columns to keep
    columns_to_keep = []
    for i in range(alignment_length):
        column = alignment[:, i]
        if column.isupper():  # Check if all characters in the column are uppercase
            columns_to_keep.append(i)
    # Filter the alignment to only include the columns to keep
    filtered_sequences = []
    for record in alignment:
        new_seq = Seq("".join([record.seq[i] for i in columns_to_keep]))
        filtered_sequences.append(
            SeqRecord(new_seq, id=record.id, description=record.description)
        )
    # Create a new alignment with the filtered sequences
    new_alignment = MultipleSeqAlignment(filtered_sequences)
    return new_alignment


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Remove columns from a multiple sequence alignment where at least one sequence has a lowercase character.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "input_file", type=str, help="Input MSA file with the alignment."
    )
    parser.add_argument(
        "output_file",
        type=str,
        help="Output MSA file to write the filtered alignment.",
    )
    parser.add_argument(
        "input_format",
        type=str,
        choices=[
            "clustal",
            "emboss",
            "fasta",
            "fasta-m10",
            "ig",
            "mauve",
            "msf",
            "nexus",
            "phylip",
            "phylip-relaxed",
            "phylip-sequential",
            "stockholm",
        ],
        help="Format of the input MSA file.",
    )
    parser.add_argument(
        "output_format",
        type=str,
        choices=[
            "clustal",
            "emboss",
            "fasta",
            "fasta-m10",
            "ig",
            "mauve",
            "msf",
            "nexus",
            "phylip",
            "phylip-relaxed",
            "phylip-sequential",
            "stockholm",
        ],
        help="Format of the output MSA file.",
    )
    parser.add_argument(
        "--remove-lowercase-columns",
        action="store_true",
        help="Remove columns with lowercase characters.",
    )

    # Print help if no arguments are provided
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    # Parse the arguments
    args = parser.parse_args()

    # Read the input alignment
    alignment = AlignIO.read(args.input_file, args.input_format)

    # Remove columns with lowercase characters
    if args.remove_lowercase_columns:
        alignment = filter_uppercase_columns(alignment)

    # Write the filtered alignment to a new file
    AlignIO.write(alignment, args.output_file, args.output_format)


if __name__ == "__main__":
    main()
