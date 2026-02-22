import os
from abc import ABC, abstractmethod
from loki import oci_builder

class Runtime(ABC):
    @abstractmethod
    def run(self):
        pass

class Container(Runtime):
    def __init__(self, parsed_cmds):
        self.cmds = parsed_cmds

    def run(self):
        pass
        
