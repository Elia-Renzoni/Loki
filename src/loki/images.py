from loki import commands as cmds

class Image:
    def __init__(self, context):
        self.context = context
        self.expected_commands = cmds.build_commands_lookup()["build"]

        self.image_name = None
        self.image_scripts = list()
        self.image_workdir = None
        self.image_copy = list()
        self.image_ports = list()
        self.image_cmds = list()

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
                self.image_scripts = value
            case "--copy":
                self.image_copy = value
            case "--workdir":
                self.image_workdir = value
            case "--expose":
                self.image_ports = value
            case "--cmd":
                self.image_cmds = value

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

