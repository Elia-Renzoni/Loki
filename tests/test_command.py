
import unittest
from loki import mng_command as cmd
from loki import cmd_parser as parser

class TestCommand(unittest.TestCase):

    def test_compile_command(self):
        argv = ["start", "container_name"]

        context = parser.parse_commands(argv)
        self.assertEqual(context.is_context_none(), False)

        command = cmd.ManagementCommand(context)
        command.compile()
        self.assertEqual(command.get_command(), "start")
        self.assertEqual(command.get_optional_target(), "container_name")

        argv = ["ps"]
        context = parser.parse_commands(argv)
        command = cmd.ManagementCommand(context)
        command.compile()
        self.assertEqual(command.get_command(), "ps")
        self.assertEqual(command.get_optional_target(), None)

if __name__ == '__main__':
    unittest.main()
