'''
mng_command.py represents the non-composite commands in Loki
'''

from loki import command as cmd

class ManagementCommand(cmd.Command):
    '''
    ManagementCommand contains the simplest commands in Loki
    e.g loki ps, loki start, loki stop, loki images
    '''
    def __init__(self, parser_context):
        self.ctx = parser_context.get_context()

        self.command = None
        self.optional_target = None

    def compile(self):
        self.command = self.ctx.get("command")
        self.optional_target = self.ctx.get("target")

    def get_command(self):
        '''
        get_command returns the command issued by the user
        '''
        return self.command

    def get_optional_target(self):
        '''
        get_optional_target returns the optional target in case
        of a start or stop commands
        '''
        return self.optional_target

