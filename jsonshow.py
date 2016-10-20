#!/usr/bin/env python
"""
Convert JSON data to human-readable form.

(Reads from stdin and writes to stdout)
"""

import sys
import json
import fileinput

if __name__ == "__main__":

    name = raw_input("input name: ")
    print name

    int_input = map(int,raw_input("your age!!! "))

    sys.stdin.readlines()
    print type(int_input), int_input
    # print json.dumps(json.loads(name), indent=4)
    # sys.exit(0)