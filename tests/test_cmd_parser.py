from loki import cmd_parser as parser
import unittest

class TestParser(unittest.TestCase):

    def test_parse_commands(self):
        argv = ["build", "--run=apt get"]
        context = parser.parse_commands(argv)
        self.assertEqual(context.is_context_none(), False)

if __name__ == '__main__':
    unittest.main()
