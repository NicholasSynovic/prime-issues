from argparse import ArgumentParser, Namespace
from importlib.metadata import version
from pathlib import Path

import prime_issues.args as argVars


def getArgs() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog=argVars.programName,
        usage="To extract relvant issue information about online hosted repositories from online issue trackers",
        epilog=f"Authors: {', '.join(argVars.authorNames)}",
        formatter_class=argVars.AlphabeticalOrderHelpFormatter,
    )
    parser.add_argument(
        "--tracker",
        default="gh",
        type=str,
        choices=["gh"],
        required=False,
        help="Set the issue tracker to collect issues from",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"{argVars.programName}: {version(distribution_name='prime-issues')}",
    )
    parser.add_argument(
        "-a",
        "--author",
        type=str,
        required=True,
        help="The author of the repository",
        dest="author",
    )
    parser.add_argument(
        "-n",
        "--name",
        type=str,
        required=True,
        help="The name of the repository",
        dest="name",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=Path("commits.json").resolve(),
        type=Path,
        required=False,
        help="Output file to store commit and SCLC data in JSON format",
        dest="output",
    )
    parser.add_argument(
        "-l",
        "--log",
        default=Path("commits.log").resolve(),
        type=Path,
        required=False,
        help="File to store logging information",
        dest="log",
    )

    return parser.parse_args()
