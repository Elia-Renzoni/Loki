import unittest
from src.loki import registry

class TestRegistry(unittest.TestCase):
    
    def test_setup_database(self):
        try:
            registry.setup_database()
        except RuntimeError as err:
            self.fail(err)

        table_names = ["env", "port", "image", "container", "cmd", "script"]
        pragma_command = "PRAGMA table_info()".format()

        for tname in table_names:
            pragma_command = "PRAGMA table_info({table_name})".format(table_name=tname)
            registry.middleware.execute(pragma_command)
            self.assertIsNone(registry.middleware.fetchone())

if __name__ == '__main__':
    unittest.main()
