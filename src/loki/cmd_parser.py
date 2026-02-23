"""
CLI argument parser for Loki.

This module defines the command-line interface and returns
a ParserContext containing the parsed arguments.
"""

import argparse

from loki import commands


class ParserContext:
    """Wrapper around argparse Namespace."""

    def __init__(self, namespace) -> None:
        """Initialize parser context from argparse namespace."""
        self.context = vars(namespace)

    def is_context_none(self) -> bool:
        """Return True if context is empty."""
        return not self.context

    def get_context(self):
        """Return parsed context as dictionary."""
        return self.context


def parse_commands(args) -> ParserContext:
    """
    Parse CLI arguments and return a ParserContext instance.
    """
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    cmd_lookup = commands.build_commands_lookup()

    for cmd, subcmds in cmd_lookup.items():
        subparser = subparsers.add_parser(cmd)

        # Commands without subcommands (e.g. ps, images, rm)
        if subcmds is None:
            if cmd in ("start", "stop"):
                subparser.add_argument("target")
            continue

        # Commands with options
        for option in subcmds:
            if option in {
                "--env",
                "--run",
                "--expose",
                "--port",
                "--copy",
                "--cmd",
            }:
                subparser.add_argument(
                    option,
                    action="append",
                )
            else:
                subparser.add_argument(option)

    result = parser.parse_args(args)
    return ParserContext(result)

