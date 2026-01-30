import unittest
from loki import registry

class TestRegistry(unittest.TestCase):
    
    def test_setup_database(self):
        try:
            registry.setup_database()
        except RuntimeError as err:
            self.fail(err)

        table_names = ["env", "port", "image", "container", "cmd", "copy", "script"]

        for tname in table_names:
            conn = registry.middleware.connection
            csr = conn.cursor()
            csr.execute(
                    "PRAGMA table_info({table_name});".format(table_name=tname)
            )
            database_schema = csr.fetchall()
            print(database_schema)
            self.assertGreaterEqual(len(database_schema), 0, "{table_name} is empty".format(table_name=tname))

if __name__ == '__main__':
    unittest.main()
