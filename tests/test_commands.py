from src.loki import commands
import unittest

class TestCommands(unittest.TestCase):

    def test_build_commands_lookup(self):
        lookup = commands.build_commands_lookup()
        if lookup.keys() not in ["build", "run", "start", "stop", "ps", "images"]:
            self.fail("lookup failed")

if __name__ == '__main__':
    unittest.main()
