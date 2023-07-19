#!/usr/bin/env python3.11

"""Module for counting occurences in string"""

string = input("Enter a string: ")
occurences = {}
for ch in string:
    occurences.setdefault(ch, 0)
    occurences[ch] += 1
sorted_occurences = sorted(occurences.items(), key=lambda x:x[1], reverse=True)
for item in sorted_occurences:
    print(f"{item[0]}: {item[1]}", end=" ")
