import sys
from loki import cmd_parser as parser
from loki import command_handlers as handler
import os

def loki_start(argv=None):
    context = parser.parse_commands(argv)
    if context.is_context_none():
        os._exit(1)

    handler.read_command(context)
    handler.exec(context.get_context())

if __name__ == '__main__':
    loki_start(sys.argv[0:])
