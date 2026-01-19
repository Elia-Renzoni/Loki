import unittest
from loki import images
from loki import cmd_parser as parser


class TestImages(unittest.TestCase):

    def test_compile_image(self):
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

        self.assertEqual(img.get_image_name(), "pyapp")
        self.assertEqual(img.get_image_workdir(), "/app")
        self.assertEqual(img.get_image_scripts(), ["pip install flask"])
        self.assertEqual(img.get_image_cmds(), ["python app.py"])
        self.assertEqual(img.get_image_copy_targets(), ["./src/app"])
        self.assertEqual(img.get_image_ports(), ["6060"])


if __name__ == '__main__':
    unittest.main()
