import argparse
from src.loki import commands

class ParserContext:
    def __init__(self, namespace):
        self.context = vars(namespace)
    
    def is_context_none(self):
        return self.context is None

    def get_context(self):
        return self.context

def parse_commands(args):
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(
            dest="commands", 
            required=True
    )

    cmd_lookup = commands.build_commands_lookup()
    sub = None
    for cmd, subcmd in cmd_lookup.items():
        if subcmd is None:
            sub = subparser.add_parser(cmd)
            continue

        sub = subparser.add_parser(cmd)
        for command in subcmd:
            sub.add_argument(command)

    result = parser.parse_args(args)
    return ParserContext(result)
