"""Command dispatch and execution logic for Loki."""

from loki import images
from loki import containers
from loki import mng_command

def read_command(context):
    """Create the appropriate command object based on parsed context."""
    if context.get("build") is True:
        return images.Image(context)

    if context.get("run") is True:
        return containers.Containers(context)

    return mng_command.ManagementCommand(context)

def execute(command_obj):
    """Execute the given command object."""
    if isinstance(command_obj, images.Image):
        return create_image(command_obj)

    if isinstance(command_obj, containers.Containers):
        return run_container(command_obj)

    return run_management_command(command_obj)


def create_image(cmd):
    """Execute image build command."""
    # TODO: implement image build logic
    return None


def run_container(cmd):
    """Execute container run command."""
    # TODO: implement container runtime logic
    return None


def run_management_command(cmd):
    """Execute management command."""
    # TODO: implement management command logic
    return None

