from loki import commands as cmds

class Containers:
    def _init__(self, context):
        self.lookup = cmds.build_commands_lookup()
        self.expected_commands = self.lookup['build']
        self.context = context

    def compile_container(self):
        pass
