#!/usr/bin/env python3.11

"""Module to create a tuple of unique numbers from the user input"""

NUM_LIST = list(map(int, input("Enter several numbers: ").split()))
NUM_TUPLE = tuple(set(NUM_LIST))
print("Tuple of unique numbers:", NUM_TUPLE)
