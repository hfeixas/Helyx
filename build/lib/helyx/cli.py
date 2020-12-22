#!/usr/bin/python3 -u

import sys
import os


def main():
    """
    Main CLI Runner.
    """
    python = sys.executable
    os.execvp(python, [python] + sys.argv[1:])
