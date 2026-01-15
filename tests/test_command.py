
import unittest
from loki import command as cmd
from loki import cmd_parser as parser

class TestCommand(unittest.TestCase):

    def test_compile_command(self):
        argv = ["start", "peppe"]

        context = parser.parse_commands(argv)
        self.assertEqual(context.is_context_none(), False)

        command = cmd.ManagementCommand(context)
        self.assertEqual(command.get_command(), "start")
        self.assertEqual(command.get_optional_target(), "peppe")

if __name__ == '__main__':
    unittest.main()
