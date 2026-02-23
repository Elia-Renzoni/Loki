"""Command and subcommand definitions for Loki CLI."""


def build_commands_lookup():
    """Return a lookup table for supported commands and subcommands."""
    return {
        "build": get_build_subcommands(),
        "run": get_run_subcommands(),
        "ps": None,
        "start": None,
        "stop": None,
        "images": None,
        "rm": None,
    }


def get_build_subcommands() -> list[str]:
    """Return supported subcommands for the build command."""
    return [
        "--name",
        "--run",
        "--expose",
        "--copy",
        "--workdir",
        "--cmd",
    ]


def get_run_subcommands() -> list[str]:
    """Return supported subcommands for the run command."""
    return [
        "--name",
        "--env",
        "--mount",
        "--port",
    ]

