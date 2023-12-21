#!/usr/bin/env python
""" Merge the pdfs supplied on the command line - the last file is the output
   """

import argparse
import os
import sys
from importlib.metadata import version

from pypdf import PdfWriter

# import shutil
# from PyPDF2 import PdfMerger


class MyException(Exception):
    """Generic exception to avoid pylint errors"""


class PdfMerge:
    """Merge the pdfs supplied on the command line - the last file is the output"""

    parser = None

    def __init__(self):
        self.input_files = []
        self.output_file = None
        self.make_cmd_line_parser()
        self.version = None
        self.overwrite = False
        self.make_cmd_line_parser()
        self.parse_args()

    def make_cmd_line_parser(self):
        """Set up the command line parser"""

        self.parser = argparse.ArgumentParser(
            description="Merge the pdfs supplied on the command line"
        )
        self.parser.add_argument(
            "-i",
            "--input_file",
            action="append",
            help="Input PDF files (>=2)",
        )
        self.parser.add_argument(
            "-V",
            "--version",
            action="version",
            version=version("dml-pdfmerge"),
            help="Print the version number",
        )
        self.parser.add_argument(
            "--overwrite",
            action="store_true",
            default=False,
            help="Do not overwrite existing output",
        )
        self.parser.add_argument("output_file")

    def parse_args(self):
        """Parse the command line arguments"""
        args = self.parser.parse_args()
        self.input_files = args.input_file
        self.output_file = args.output_file
        self.overwrite = args.overwrite

    def validate_args(self):
        """Validate the command line arguments"""
        if len(self.input_files) < 2:
            self.parser.print_help()
            sys.exit(1)
        if not self.output_file:
            self.parser.print_help()
            sys.exit(1)

    def process_args(self):
        """Process the command line arguments"""
        self.parse_args()
        self.validate_args()

    def run(self):
        """Merge the pdfs supplied on the command line - the last file is the output"""
        self.validate_args()
        if os.path.exists(self.output_file) and not self.overwrite:
            raise MyException(
                f"Output file {self.output_file} already exists (Use '--overwrite' if neccessary)"
            )
        merger = PdfWriter()
        for input_file in self.input_files:
            if not os.path.exists(input_file):
                raise MyException(f"Input file {input_file} does not exist")
            merger.append(input_file)
        merger.write(self.output_file)
        merger.close()
        print(f"Output file {self.output_file} created")


def main():
    """Main entry point"""
    try:
        PdfMerge().run()
    except MyException as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
