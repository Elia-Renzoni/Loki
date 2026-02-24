import unittest

from loki import oci_builder as builder
from loki import images
from loki import cmd_parser as parser
from loki import containers as cnt

class TestImageBuilder(unittest.TestCase):
    def test_run(self):
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
        img = images.Image(context.get_context())
        img.compile()

        b = builder.ImageBuilder(img)
        b.run()

        self.assertNotEqual(b._fs_layers["root_fs"], None)
        print(b._fs_layers["root_fs"])
        self.assertNotEqual(b._fs_layers["history"], None)
        print(b._fs_layers["history"])

if __name__ == "__main__":
    unittest.main()
