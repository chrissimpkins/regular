#!/usr/bin/env python3

import cProfile
import pstats
from io import StringIO

import regular
import re


def profile():
    # ------------------------------------------------------------------------------
    # Setup a profile
    # ------------------------------------------------------------------------------
    pr = cProfile.Profile()
    # ------------------------------------------------------------------------------
    # Enter setup code below
    # ------------------------------------------------------------------------------
    # Optional: include setup code here

    with open("1468-6708-3-4.txt", "r") as f:
        text = f.read()

    # ------------------------------------------------------------------------------
    # Start profiler
    # ------------------------------------------------------------------------------
    pr.enable()

    # ------------------------------------------------------------------------------
    # BEGIN profiled code block
    # ------------------------------------------------------------------------------
    regex = regular.compile("[Tt]o")
    for _ in range(10000):
        # re.search("[Tt]o", text)
        # re.sub("[Tt]o", "01", text)
        regex.replace_all(text, "01")

    # ------------------------------------------------------------------------------
    # END profiled code block
    # ------------------------------------------------------------------------------
    pr.disable()
    s = StringIO()
    sortby = "cumulative"
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.strip_dirs().sort_stats("time").print_stats()
    print(s.getvalue())


if __name__ == "__main__":
    profile()
