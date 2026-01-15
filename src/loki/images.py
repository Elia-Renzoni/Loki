from loki import commands as cmds

class Image:
    def __init__(self, context):
        self.context = context
        self.expected_commands = cmds.build_commands_lookup()["build"]

        self.image_name = None
        self.image_scripts = set()
        self.image_workdir = set()
        self.image_copy = set()
        self.image_ports = set()
        self.image_cmds = set()

    def compile_image(self):
        for exp_cmd in self.expected_commands:
            key = exp_cmd.lstrip("-")
            value = self.context.get(key)

            if value is not None:
                value = self._clean_value(value)
                self._fill_image_fields(exp_cmd, value)

    def _clean_value(self, value):
        if isinstance(value, str):
            return value.strip("'").strip('"')
        return value

    def _fill_image_fields(self, cmd, value):
        match cmd:
            case "--name":
                self.image_name = value
            case "--run":
                self.image_scripts.add(value)
            case "--copy":
                self.image_copy.add(value)
            case "--workdir":
                self.image_workdir.add(value)
            case "--expose":
                self.image_ports.add(value)
            case "--cmd":
                self.image_cmds.add(value)

    def get_image_name(self):
        return self.image_name

    def get_image_workdir(self):
        return self.image_workdir

    def get_image_scripts(self):
        return self.image_scripts

    def get_image_cmds(self):
        return self.image_cmds

    def get_image_copy_targets(self):
        return self.image_copy

    def get_image_ports(self):
        return self.image_ports

