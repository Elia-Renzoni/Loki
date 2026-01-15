from loki import commands as cmds

class Image:
    def __init__(self, context):
        self.lookup = cmds.build_commands_lookup()
        self.expected_commands = self.lookup['build']
        self.context = context
        self.image_name = None
        self.image_scripts = set()
        self.image_workdir = None
        self.image_copy = set()
        self.image_entrypoint = set()
        self.image_ports = set()
        self.image_cmds = set()

    def compile_image(self):
        for exp_cmd in self.expected_commands:
           if exp_cmd in self.context: 
               self.fill_image_fields(exp_cmd, self.context[exp_cmd])

    def fill_image_fields(self, cmd, value):
        match cmd:
            case "--name":
                self.image_name = value
            case "--run":
                self.image_scripts.add(value)
            case "--copy":
                self.image_copy.add(value)
            case "--entrypoint":
                self.image_entrypoint.add(value)
            case "--workdir":
                self.image_workdir = value
            case "--expose":
                self.image_ports.add(value)
            case "--cmd":
                self.image_cmds.add(value)
            case _:
                raise Exception

    def get_image_name(self):
        return self.image_name

    def get_image_cmds(self):
        return self.image_cmds

    def get_image_scripts(self):
        return self.get_image_scripts

    def get_image_copy_targets(self):
        return self.image_copy

    def get_image_workdir(self):
        return self.image_workdir

    def get_image_entrypoints(self):
        return self.image_entrypoint

    def get_image_ports(self):
        return self.image_ports
