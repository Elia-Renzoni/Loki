#!/usr/bin/env python3

"""Loki CLI entry point."""

import os
import sys

from loki import cmd_parser
from loki import command_handlers


def loki_start(argv=None):
    """Start Loki CLI and dispatch the command."""
    context = cmd_parser.parse_commands(argv)

    if context.is_context_none():
        os._exit(1)

    command_handlers.read_command(context)
    command_handlers.execute(context.get_context())


if __name__ == "__main__":
    loki_start(sys.argv[1:])

