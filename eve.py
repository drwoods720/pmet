#!/usr/bin/env python3

import os
import argparse
import src.main as main

title: str = r'''
 _____      _____
|  ___|    |  ___|
| |____   _| |__
|  __\ \ / /  __|
| |___\ V /| |___
\____(_)_(_)____/
(EvE)aluates Various modEls

Please put on your 3d glasses now.
'''

def run() -> None:
    parser = argparse.ArgumentParser(
        description="(EvE)aluates Various modEls"
    )

    parser.add_argument("-i", "--input", type=str, help="Input directory.")
    parser.add_argument("-o", "--output", type=str, help="Output directory")
    parser.add_argument("-c", "--code", type=str, help="Cheat codes")

    args = parser.parse_args()

    if args.code == "uuddlrlrba":
        # Super mode activated!
        print("[31mS[0m[33mU[0m[32mP[0m[36mE[0m[34mR[0m [35mM[0m[31mO[0m[33mD[0m[32mE[0m [36mA[0m[34mC[0m[35mT[0m[31mI[0m[33mV[0m[32mA[0m[36mT[0m[34mE[0m[35mD[0m[31m![0m")
        print(title[::-1])
    else:
        print(title)

    input_dir: str | None = None
    output_dir: str = args.output

    if args.input:
        input_dir = args.input
    else:
        print("No input directory specified!")
        print("Try '-h' or '--help' for more information.")
        exit()

    if not os.path.isdir(input_dir):
        print(f"Invalid directory {input_dir} entered!")
        print("Please check your parameters and try again.")
        exit()

    print(f"Input: {input_dir} \nOutput: {output_dir}")

    if args.output:
        main.run(input_dir, args.output)
    else:
        main.run(input_dir)

    print("Processing complete!")
    print("Thank you for using EvE, You can now take off your 3d glasses.")

if __name__ == "__main__":
    run()
