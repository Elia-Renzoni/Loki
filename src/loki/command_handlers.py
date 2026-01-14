from loki import images
from loki import containers
from loki import command

def read_commands(context):
    if context['build'] is True:
        return images.Image(context)
    elif context['run'] is True:
        return containers.Containers(context)
    else:
        return command.Command()

def select_handler():
    pass
