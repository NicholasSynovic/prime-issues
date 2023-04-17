import logging
from argparse import Namespace
from logging import FileHandler, Formatter, Logger
from pathlib import Path
from typing import List

from pandas import DataFrame


class Config:
    def __init__(self, args: Namespace) -> None:
        self.AUTHOR: Path = args.author
        self.REPO_NAME: str = args.name
        self.OUTPUT: Path = args.output.resolve()
        self.LOG: Path = args.log.resolve()
        self.DF_LIST: List[DataFrame] = []
        self.LOGGER = Logger(name="PRIME Issues Collector", level=logging.INFO)

        logFileHandler: FileHandler = FileHandler(filename=self.LOG)
        logDateFormat: Formatter = Formatter(
            fmt="%(asctime)s %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        logFileHandler.setFormatter(fmt=logDateFormat)
        self.LOGGER.addHandler(hdlr=logFileHandler)

        self.TRACKER: int
        match args.tracker:
            case "gh":
                self.SCLC = 0
                self.LOGGER.info(msg=f"Using GitHub Issues as the Issue Tracker")
            case _:
                exit(1)
