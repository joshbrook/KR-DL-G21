import argparse
from pathlib import Path
from dataclasses import dataclass


from .reasoner import ELReasoner

from typing import List


@dataclass
class Args:
    input_file: Path
    class_name: str


def parse_arguments(args: List[str]) -> Args:
    parser = argparse.ArgumentParser(
        prog="The EL reasoner from group 21",
    )
    parser.add_argument(
        "input_file",
        help="The file to load the ontology of",
        # This cannot be an argparse.FilePath because the JVM is scuffed
        # To be more precise, the JVM thinks the filepath is relative to itself,
        # meaning we have to resolve it to an absolute path before passing
        type=str,
    )

    parser.add_argument(
        "class_name",
        help="The class to get all the subsumers from",
        type=str,
    )
    arguments = parser.parse_args(args)

    return Args(Path(arguments.input_file).resolve(), arguments.class_name)


def run(args: Args) -> None:
    for item in ELReasoner(
        str(args.input_file), ["0", "1", "2", "3", "4", "5"]
    ).get_all_subsumers(args.class_name):
        print(item)


def main(args: List[str]) -> None:
    run(parse_arguments(args))
