import unittest
from loki import images 
from loki import command as cmd
from loki import cmd_parser as parser


class TestImages(unittest.TestCase):

    def test_compile_image(self):
        argv = [
                "build", 
                "--name=pyapp", 
                "--run='pip install flask'", 
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

        self.assertEqual(img.get_image_name(), None)
        self.assertEqual(img.get_image_workdir(), set().add("/app"))
        self.assertEqual(img.get_image_scripts(), set().add("pip install flask"))
        self.assertEqual(img.get_image_cmds(), set().add("python app.py"))
        self.assertEqual(img.get_image_copy_targets(), set().add("./src/app"))
        self.assertEqual(img.get_image_ports(), set().add("6060"))


if __name__ == '__main__':
    unittest.main()
        
