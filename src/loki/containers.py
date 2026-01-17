from loki import commands as cmds

class Containers:
    def __init__(self, context):
        self.lookup = cmds.build_commands_lookup()
        self.expected_commands = self.lookup['run']
        self.context = context
        self.container_envs = list()
        self.container_mount = None
        self.container_name = None
        self.container_ports = list()

    def compile_container(self):
        for exp_cmd in self.expected_commands:
            key = exp_cmd.lstrip("-")
            value = self.context.get(key)
            print(value)

            if value is not None:
                self.fill_container_fields(value, exp_cmd)

    def fill_container_fields(self, value, cmd):
        match cmd:
            case "--env":
                self.container_envs = value
            case "--mount":
                self.container_mount = value
            case "--name":
                self.container_name = value
            case "--port":
                self.container_ports = value

    def get_container_name(self):
        return self.container_name

    def get_container_envs(self):
        return self.container_envs

    def get_container_mount(self):
        return self.container_mount

    def get_container_ports(self):
        return self.container_ports
