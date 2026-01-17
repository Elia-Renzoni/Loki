
def build_commands_lookup():
    commands_lookup = dict()
    commands_lookup["build"] = get_build_subcommands()
    commands_lookup["run"] = get_run_subcommands()
    commands_lookup["ps"] = None
    commands_lookup["start"] = None
    commands_lookup["stop"] = None
    commands_lookup["images"] = None
    commands_lookup["rm"] = None

    return commands_lookup

def get_build_subcommands():
    return [
            "--name",
            "--run",
            "--expose",
            "--copy",
            "--workdir",
            "--cmd"
    ]

def get_run_subcommands():
    return [
            "--name",
            "--env",
            "--mount",
            "--port",
    ]
    
