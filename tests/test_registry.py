import unittest
from loki import registry
from loki import images
from loki import cmd_parser as parser

class TestRegistry(unittest.TestCase):

    full_image_snapshot = """
    """
    
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

    def test_add_image(self):
        argv = [
                "build", 
                "--name=pyapp", 
                "--run=pip install flask", 
                "--copy=./src/app",
                "--workdir=/app",
                "--expose=6060",
                "--cmd=python app.py",
        ]

        context = parser.parse_commands(argv)
        self.assertEqual(context.is_context_none(), False)
        print(context)

        img = images.Image(context.get_context())
        img.compile_image()

        registry.add_image(img)

        # TODO-> take a full snapshot and check the results with assert

if __name__ == '__main__':
    unittest.main()
