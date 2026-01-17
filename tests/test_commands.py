from loki import commands
import unittest

class TestCommands(unittest.TestCase):

    def test_build_commands_lookup(self):
        lookup = commands.build_commands_lookup()
        print(lookup)
        exp_keys = ["build", "run", "start", "stop", "ps", "images", "rm"]
        self.assertEqual(set(exp_keys), set(lookup.keys()))

if __name__ == '__main__':
    unittest.main()
