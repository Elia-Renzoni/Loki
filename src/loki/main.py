import sys
import cmd_parser as parser
import os

def loki_start(argv=None):
    context = parser.parse_commands(argv)
    if context.is_context_none():
        os._exit(1)

if __name__ == '__main__':
    loki_start(sys.argv[0:])
