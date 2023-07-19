#!/usr/bin/env python3.11

"""Module to find file extension """
import sys

if len(sys.argv) != 2:
    print ("You should provide one argument: a filename")
    sys.exit(1)
DOT_PLACE = sys.argv[1].find('.')
if DOT_PLACE in (-1, len(sys.argv[1]) - 1):
    raise RuntimeError("The file has no extension!")
print(f"The extension of file is {sys.argv[1][DOT_PLACE + 1:]}")
