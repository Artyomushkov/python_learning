#!/usr/bin/env python3.11

"""Module for analyzing access.log file"""

import sys

if len(sys.argv) != 2:
    print ("There should be one argument: the name of file")
    sys.exit(1)
stats = {}
with open(sys.argv[1], "r", encoding="utf-8") as file:
    for line in file:
        begin_index = line.rfind('"', 0, len(line) - 2)
        user_agent = line[begin_index + 1 : len(line) - 2]
        stats.setdefault(user_agent, 0)
        stats[user_agent] += 1
print(f"Total user agents: {len(stats)}")
sorted_stats = dict(sorted(stats.items(), key=lambda x:x[1], reverse=True))
for item in sorted_stats.items():
    print(f"User agent: {item[0]} Request number: {item[1]}")
