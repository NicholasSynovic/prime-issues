from argparse import Namespace
from warnings import filterwarnings

from prime_issues.args.issuesArgs import getArgs
from prime_issues.trackers import gh
from prime_issues.utils.config import Config

filterwarnings(action="ignore")


def main() -> None:
    args: Namespace = getArgs()
    config: Config = Config(args=args)

    match args.tracker:
        case "gh":
            gh.main(config=config)
        case _:
            exit(1)


if __name__ == "__main__":
    main()
