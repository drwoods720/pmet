#!/usr/bin/env python3

# E.V.E - Evalutates Various modeEls

import os
import src.run as run

title = """
 _____      _____
|  ___|    |  ___|
| |____   _| |__
|  __\ \ / /  __|
| |___\ V /| |___
\____(_)_(_)____/
(EvE)aluates Various modEls
"""

def setInputDirectory() -> str:
    while True:
        print("Please enter the input directory or EXIT to exit")
        user_input = input("Input directory: ")

        if user_input == "EXIT":
            print("Exiting...")
            return ""
        elif os.path.isdir(user_input):
            return user_input
        else:
            print(f"Invalid directory {user_input} entered!")
            input()

def setThreading() -> bool:
    while True:
        print("Would you like to enable multithreading?")
        user_input: str = input("(y/n): ").lower()

        if user_input.lower() == "y":
            print("Multithreading enabled!")
            print("Warning! Multithreading is an experemental feature and may not work as expected!")
            return True
        if user_input.lower() == "n":
            print("Multithreading disabled!")
            return False
        else:
            print(f"Unknown option {user_input}")


def mainMenu(title: str) -> None:
    input_directory: str = ""
    multithreading: bool = False

    while(True):
        print(title)
        print("(I)nput directory")
        print("(M)ultithreading")
        print("(R)un")
        print("(E)xit")

        selection: str = input("Selection: ")
        selection_lower = selection.lower()[0]


        if selection_lower == "e":
            break
        elif selection_lower == "r":
            if input_directory != "":
                run.run(input_directory, multithreading)
                print("Processing Complete!")
                exit()
            else:
                print("No input directory set!")
            print("Press enter key to continue...")
            input()
        elif selection_lower == "i":
            input_directory = setInputDirectory()
            print(f"input directory set to {input_directory}")
            print("Press enter to continue")
            input()
        elif selection_lower == "m":
            multithreading = setThreading()
        # Small easter egg
        elif selection == "uuddlrlrbastart":
            print("Super Mode activated!")
        else:
            print(f"Unknown option {selection}")
            print("Please try again")


    print("Thank you, please come again!")

def main():
    mainMenu(title)

if __name__ == "__main__":
    main()
