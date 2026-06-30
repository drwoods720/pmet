#!/usr/bin/env python3

import os
import argparse
from typing import Any

import src.main as main

TITLE: str = r"""
 _____      _____
|  ___|    |  ___|
| |____   _| |__
|  __\ \ / /  __|
| |___\ V /| |___
\____(_)_(_)____/
(EvE)aluates Various modEls
Please put on your 3d glasses now.
"""


def eve() -> None:
    """
    The user interface for the eve program.
    """
    parser = argparse.ArgumentParser(description="(EvE)aluates Various modEls")

    _ = parser.add_argument("-i", "--input", type=str, help="input directory")
    _ = parser.add_argument("-o", "--output", type=str, help="output directory")
    _ = parser.add_argument(
        "-w", "--workers", type=int, help="maximum number of parallel processes"
    )

    # Hidden cheat code argument
    _ = parser.add_argument("cheatcode", nargs="?", help=argparse.SUPPRESS)

    args = parser.parse_args()

    # Small easter egg
    if args.cheatcode == "uuddlrlrba":
        # Super mode activated!
        print(
            "[31mS[0m[33mU[0m[32mP[0m[36mE[0m[34mR[0m [35mM[0m[31mO[0m[33mD[0m[32mE[0m [36mA[0m[34mC[0m[35mT[0m[31mI[0m[33mV[0m[32mA[0m[36mT[0m[34mE[0m[35mD[0m[31m![0m"
        )
        print(TITLE[::-1])
    else:
        print(TITLE)

    kwargs: dict[str, Any] = {
        "root_dir": args.input,
    }

    if args.output:
        kwargs["output_dir"] = args.output
    if args.workers:
        kwargs["max_workers"] = args.workers

    # Input validation
    if not args.input:
        print("No input directory specified!")
        print("Try '-h' or '--help' for more information.")
        exit()

    if not os.path.isdir(kwargs["root_dir"]):
        print(f"Invalid directory {kwargs['root_dir']} entered!")
        print("Please check your parameters and try again.")
        exit()

    main.run(**kwargs)

    print("Processing complete!")
    print("Thank you for using EvE, You can now take off your 3d glasses.")


if __name__ == "__main__":
    eve()
