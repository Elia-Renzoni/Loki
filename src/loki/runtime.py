from abc import ABC, abstractmethod

class Runtime(ABC):
    @abstractmethod
    def run(self):
        pass

class Container(Runtime):
    def __init__(self, parsed_cmds):
        self.cmds = parsed_cmds

    def run(self):
        pass
        
class Image(Runtime):
    def __init__(self, parsed_cmds):
        self.cmds = parsed_cmds

    def run(self):
        name = self.cmds.get_image_name()
