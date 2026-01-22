"""Image build logic for Loki."""

from loki import commands as cmds
from loki import command as cmd


class Image(cmd.Command):
    """Represents a container image build configuration."""

    def __init__(self, context):
        """Initialize image with parsed CLI context."""
        self.context = context
        self.expected_commands = cmds.build_commands_lookup()["build"]

        self.image_name = None
        self.image_scripts = []
        self.image_workdir = None
        self.image_copy = []
        self.image_ports = []
        self.image_cmds = []

    def compile(self):
        """Compile image configuration from CLI context."""
        for exp_cmd in self.expected_commands:
            key = exp_cmd.lstrip("-")
            value = self.context.get(key)

            if value is not None:
                cleaned = self._clean_value(value)
                self._fill_image_fields(exp_cmd, cleaned)

    def _clean_value(self, value):
        """Clean string values from quotes."""
        if isinstance(value, str):
            return value.strip("'").strip('"')
        return value

    def _fill_image_fields(self, cmd, value):
        """Dispatch command values to image fields."""
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
        """Return image name."""
        return self.image_name

    def get_image_workdir(self):
        """Return image working directory."""
        return self.image_workdir

    def get_image_scripts(self):
        """Return build scripts."""
        return self.image_scripts

    def get_image_cmds(self):
        """Return image commands."""
        return self.image_cmds

    def get_image_copy_targets(self):
        """Return copy targets."""
        return self.image_copy

    def get_image_ports(self):
        """Return exposed ports."""
        return self.image_ports

