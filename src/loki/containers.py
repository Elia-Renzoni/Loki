"""Container runtime logic for Loki."""

from loki import commands as cmds
from loki import command as cmd


class Containers(cmd.Command):
    """Represents a container runtime configuration."""

    def __init__(self, context):
        """Initialize container configuration from CLI context."""
        self.context = context
        self.lookup = cmds.build_commands_lookup()
        self.expected_commands = self.lookup["run"]

        self.container_envs: list[str] = []
        self.container_mount: str = ""
        self.container_name: str  = ""
        self.container_ports = []

    def compile(self) -> None:
        """Compile container configuration from CLI context."""
        for exp_cmd in self.expected_commands:
            key = exp_cmd.lstrip("-")
            value = self.context.get(key)

            if value is not None:
                self._fill_container_fields(exp_cmd, value)

    def _fill_container_fields(self, cmd, value) -> None:
        """Dispatch command values to container fields."""
        match cmd:
            case "--env":
                self.container_envs = value
            case "--mount":
                self.container_mount = value
            case "--name":
                self.container_name = value
            case "--port":
                self.container_ports = value

    def get_container_name(self) -> str:
        """Return container name."""
        return self.container_name

    def get_container_envs(self) -> list[str]:
        """Return container environment variables."""
        return self.container_envs

    def get_container_mount(self) -> str:
        """Return container mount path."""
        return self.container_mount

    def get_container_ports(self):
        """Return container port mappings."""
        return self.container_ports

