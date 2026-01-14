from loki import commands as cmds

class Containers:
    def __init__(self, context):
        self.lookup = cmds.build_commands_lookup()
        self.expected_commands = self.lookup['run']
        self.context = context
        self.container_envs = set()
        self.container_runs = set()
        self.container_name = None
        self.container_ports = None

    def compile_container(self):
        for exp_cmd in self.expected_commands:
            if self.context[exp_cmd] is True:
                self.fill_container(self.context[exp_cmd], exp_cmd)


    def fill_container(self, value, cmd):
        match cmd:
            case "-r":
                pass
            case "-v":
                pass
            case "-w":
                pass
            case "-name":
                pass
