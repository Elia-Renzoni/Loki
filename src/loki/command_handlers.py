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

def exec(command_obj):
    execution_res = None
    if command_obj is images.Image:
        execution_res = create_image(command_obj)
    elif command_obj is containers.Containers:
        execution_res = create_container(command_obj)
    else:
        execution_res = create_command(command_obj)
    return execution_res

def create_image(cmd):
    pass

def create_container(cmd):
    pass

def create_command(cmd):
    pass

