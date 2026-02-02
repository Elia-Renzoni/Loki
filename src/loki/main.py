#!/usr/bin/env python3

"""Loki CLI entry point."""

import os
import sys

from loki import cmd_parser
from loki import command_handlers
from loki import registry


def loki_start(argv=None):
    """Start Loki CLI and dispatch the command."""
    context = cmd_parser.parse_commands(argv)

    if context.is_context_none():
        os._exit(1)

    try:
        registry.setup_database()
    except Exception as e:
        print(e)
        os._exit(1)

    target = command_handlers.read_command(context)
    target.compile()
    try:
        command_handlers.execute(target)
    except:
        os._exit(1)

if __name__ == "__main__":
    loki_start(sys.argv[1:])
