#!/usr/bin/python3 -u

import sys
import os

# from .actions import Action
# Need to write logic for windows folder locations, vs linux

# tfmake_managed_commands = [
#     "init", "plan", "debug", "version", 
# ]
def main():
    """
    Everything we want to wrap before we release the command
    and its child argumentes to terraform cli. If the first sys
    argument is not mapped, we release the call to terraform.
    """
    # version = pkg_resources.require("helyx")[0].version
    # if "version" in sys.argv[1]:
    #     print(version)
    #     arg = sys.argv[1].split('-')[0]
    #     target_environment = sys.argv[1].split('-')[1]
    # else:
    #     arg = sys.argv[1]
    #     target_environment = None

    # Need a better way to do this.
    python = sys.executable
    # try:
    #     current_action = Action(arg, target_environment)
    #     func = getattr(current_action, arg)
    #     func()
    # except AttributeError as E:
    #     print(str(E))
    #     if len(sys.argv) > 1:
    #         print("tfmake terraform: %s" % " ".join(sys.argv[1:]))
    os.execvp(python, [python] + sys.argv[1:])