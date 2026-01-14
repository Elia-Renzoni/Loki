from loki import images
from loki import containers
from loki import command

def read_command(context):
    if context['build'] is True:
        return images.Image(context)
    elif context['run'] is True:
        return containers.Containers(context)
    else:
        return command.Command(context)

def select_handler(command_obj):
    if command_obj is images.Image:
        create_image(command_obj)
    elif command_obj is containers.Containers:
        create_container(command_obj)
    else:
        create_command(command_obj)


def create_image(cmd):
    pass

def create_container(cmd):
    pass

def create_command(cmd):
    pass

