class ManagementCommand:
    def __init__(self, parser_context):
        ctx = parser_context.get_context()

        self.command = ctx.get("commands")
        self.optional_target = ctx.get("target")

    def get_command(self):
        return self.command

    def get_optional_target(self):
        return self.optional_target

