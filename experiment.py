from pathlib import Path
from dataclasses import dataclass
import argparse
import itertools
import time

from typing import List
from el_reasoner import ELReasoner


@dataclass
class Args:
    input_file: Path
    class_name: str
    order: List[str]


def parse_arguments() -> Args:
    parser = argparse.ArgumentParser(
        prog="The EL reasoner from group 21",
    )
    parser.add_argument(
        "input_file",
        help="The file to load the ontology of",
        type=str,
    )

    parser.add_argument(
        "class_name",
        help="The class to get all the subsumers from",
        type=str,
    )
    parser.add_argument(
        "order", help="The order the rules will be applied in", type=str
    )
    arguments = parser.parse_args()

    return Args(
        Path(arguments.input_file).resolve(),
        arguments.class_name,
        arguments.order.strip().split(","),
    )


class Timer:
    def __init__(self, name: str) -> None:
        self.name = name

    def __enter__(self) -> None:
        self.start_time = time.perf_counter_ns()

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        print(self.name, time.perf_counter_ns() - self.start_time)


# def main():
#     args = parse_arguments()
#     for order in itertools.permutations(args.order[1:]):
#         with Timer("normal"):
#             for item in ELReasoner(
#                 str(args.input_file), ["0", "1"] + list(order)
#             ).get_all_subsumers(args.class_name):
#                 print(item)


def main():
    args = parse_arguments()
    for order in [args.order, reversed(args.order)]:
        with Timer("normal"):
            for item in ELReasoner(str(args.input_file), list(order)).get_all_subsumers(
                args.class_name
            ):
                print(item)


if __name__ == "__main__":
    main()
