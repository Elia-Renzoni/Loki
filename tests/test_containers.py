import unittest
from loki import containers as cnt
from loki import cmd_parser as parser


class TestContainers(unittest.TestCase):

    def test_compile_containers(self):
        argv = [
                           "run",
                           "--name=mycnt", 
                           "--env=DB-HOST=localhost",
                           "--env=DB-PORT=5050",
                           "--mount=/data",
                           "--port=8080:80",
                           ]

        context = parser.parse_commands(argv)
        self.assertEqual(context.is_context_none(), False)
        print(context.get_context())

        container = cnt.Containers(context.get_context())
        container.compile()

        self.assertEqual(container.get_container_name(), "mycnt")
        self.assertEqual(container.get_container_envs(), ["DB-HOST=localhost", "DB-PORT=5050"])
        self.assertEqual(container.get_container_mount(), "/data")
        self.assertEqual(container.get_container_ports(), ["8080:80"])


if __name__ == "__main__":
    unittest.main()
