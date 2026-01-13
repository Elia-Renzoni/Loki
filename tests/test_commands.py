from src.loki import commands
import unittest

class TestCommands(unittest.TestCase):

    def test_build_commands_lookup(self):
        lookup = commands.build_commands_lookup()
        exp_keys = ["build", "run", "start", "stop", "ps", "images"]
        if lookup.keys() not in exp_keys:
            self.fail("lookup failed")

if __name__ == '__main__':
    unittest.main()
