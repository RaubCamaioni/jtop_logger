#!/usr/bin/python3

from jtop import jtop, JtopException
import argparse

import logging
from logging.handlers import TimedRotatingFileHandler
from logging import Formatter
from datetime import timedelta
import time

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Simple jtop logger')
    parser.add_argument('--file', action="store", dest="file", default="jtop.log")
    args = parser.parse_args()

    logger = logging.getLogger(__name__)
    handler = TimedRotatingFileHandler(filename=args.file, when='D', interval=1, backupCount=90, encoding='utf-8', delay=False)
    formatter = Formatter(fmt='%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    print(f"jtop logging: {args.file}")

    try:
        with jtop() as jetson:
            if jetson.ok():
                print(jetson.stats.keys())

            while jetson.ok():
                values = list(jetson.stats.values())
                values[1] = values[1].total_seconds()
                logger.info(",".join(str(v) for v in values)) 
                time.sleep(5)

    except JtopException as e:
        print(e)
    except KeyboardInterrupt:
        print("Closed with CTRL-C")
    except IOError:
        print("I/O error")

