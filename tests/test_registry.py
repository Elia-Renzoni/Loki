import unittest
import time
from loki import registry
from loki import images
from loki import cmd_parser as parser
from loki import containers as cnt

class TestRegistry(unittest.TestCase):

    _full_image_snapshot = """
    SELECT image.name, image.workdir, script.script_code, copy.target, port.port, cmd.cmd
    FROM image
    LEFT JOIN script ON script.image_id = image.image_id
    LEFT JOIN cmd ON cmd.image_id = image.image_id
    LEFT JOIN copy ON copy.image_id = image.image_id
    LEFT JOIN port ON port.image_id = image.image_id
    WHERE image.name = ?;
    """

    _full_container_snapshot = """
    SELECT container.name, container.mount, port,port, env.env_map, 
    FROM container
    LEFT JOIN port ON port.container_id = container.container_id
    LEFT JOIN env ON env.container_id = container.container_id
    WHERE container.name = ?;
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
        img.compile()

        try:
            registry.setup_database()
        except RuntimeError as err:
            self.fail(err)

        registry.add_image(img)

        registry.middleware.execute(self._full_image_snapshot, ("pyapp",))
        rows = registry.middleware.fetchall()
        self.assertGreater(len(rows), 0)
        row = rows[0]  
        name, workdir, script_code, copy_target, port, cmd = row

        self.assertEqual(name, "pyapp")
        self.assertEqual(workdir, "/app")
        self.assertEqual(script_code, "pip install flask")
        self.assertEqual(copy_target, "./src/app")
        self.assertEqual(port, 6060)
        self.assertEqual(cmd, "python app.py")
            
    def add_container(self):
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

        try:
            registry.setup_database()
        except Exception as e:
            self.fail(e)

        registry.add_container(container)

        registry.middleware.execute(self._full_container_snapshot, "mycnt")
        rows = registry.middleware.fetchall()
        self.assertGreater(len(rows), 0)
        row = rows[0]  
        name, mount, env, port = row

        self.assertEqual(name, "mycnt")
        self.assertEqual(mount, "/data")
        self.assertEqual(port, "8080:80")
        self.assertEqual(env, ["DB-HOST=localhost", "DB-PORT=5050"])

    def test_fetch_image(self):
        argv = [
                "build", 
                "--name=myImage", 
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
        img.compile()

        try:
            registry.setup_database()
        except RuntimeError as err:
            self.fail(err)

        registry.add_image(img)
        time.sleep(5)

        try:
            results = registry.fetch_image("myImage")
            for res in results:
                self.assertEqual(res['name'], "myImage")
                self.assertEqual(res['workdir'], "/app")
                self.assertEqual(res['port'], 6060)
                self.assertEqual(res['script_code'], "pip install flask")
                self.assertEqual(res['cmd'], "python app.py")
                self.assertEqual(res['target'], "./src/app")
                self.assertGreaterEqual(res['timestamp'].seconds, 5)
        except Exception as e:
            self.fail(e)

    def test_fetch_container(self):
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

        try:
            registry.setup_database()
        except Exception as e:
            self.fail(e)

        registry.add_container(container)
        time.sleep(5)

        try:
            results = registry.fetch_container("all")
            for res in results:
                self.assertEqual(res['container_name'], "mycnt")
                self.assertEqual(res['mount'], "/data")
                self.assertGreaterEqual(res['timestamp'].seconds, 5)
        except Exception as e:
            self.fail(e)

if __name__ == '__main__':
    unittest.main()
