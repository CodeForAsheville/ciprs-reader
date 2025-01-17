import argparse
import logging
import sys
import json

from ciprs_reader import VERSION
from ciprs_reader.reader import PDFToTextReader
from ciprs_reader.const import ParserMode


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("input", help="Path to CIPRS PDF document")
    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose_count",
        action="count",
        default=0,
        help="increases log verbosity for each occurence.",
    )
    parser.add_argument("--source", help="Include full source in JSON output", action="store_true")
    parser.add_argument("--mode", help="Parse mode", type=int, default=ParserMode.V1)
    parser.add_argument("--version", action="version", version="%(prog)s " + VERSION)
    parser.add_argument("--print-source", help="Include full source in JSON output and print it", action="store_true")

    args = parser.parse_args()
    formatter = logging.Formatter("%(levelname)s %(asctime)s %(name)s %(message)s")
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger = logging.getLogger("ciprs_reader")
    logger.addHandler(handler)
    logger.setLevel(max(3 - args.verbose_count, 0) * 10)

    logger.info("Running ciprs-reader on %s", args.input)
    reader = PDFToTextReader(args.input, mode=args.mode)
    save_source = args.source or args.print_source
    reader.parse(save_source=save_source)
    print(reader.json())
    if args.print_source:
        for document in json.loads(reader.json()):
            print(document['_meta']['source'])
