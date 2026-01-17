'''
command.py represents the non-composite commands in Loki
'''

class ManagementCommand:
    '''
    ManagementCommand contains the simplest commands in Loki
    e.g loki ps, loki start, loki stop, loki images
    '''
    def __init__(self, parser_context):
        ctx = parser_context.get_context()

        self.command = ctx.get("commands")
        self.optional_target = ctx.get("target")

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

