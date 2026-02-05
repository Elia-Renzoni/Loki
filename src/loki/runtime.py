import os
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
    _runtime_root_dir = "/loki-runtime/"
    _runtime_alpine_rootfs = "https://dl-cdn.alpinelinux.org/alpine/latest-stable/releases/x86_64/alpine-minirootfs-3.19.1-x86_64.tar.gz"
    _runtime_image_spec_name = "index.json"

    def __init__(self, parsed_cmds):
        self.cmds = parsed_cmds

    def run(self):
        self._init_workspace()
        self._configure()
        self._run_scripts()
        self._load_files()

    def _init_workspace(self):
        image_name = self.cmds.get_image_name()
        if image_name is None:
            pass
        target_path = self._runtime_root_dir + image_name
        os.makedirs(target_path, exist_ok=True)

        # install alpine rootfs
        import urllib.request
        import tarfile
        import io

        with urllib.request.urlopen(self._runtime_alpine_rootfs) as resp:
            with tarfile.open(fileobj=io.BytesIO(resp.read()), mode="r:gz") as tar:
                tar.extractall(target_path)

        # TODO-> create an OCI image
        json_image_path = self._runtime_root_dir + self._runtime_image_spec_name
        with open(json_image_path, "w") as f:
            self._create_oci_image(f)

    def _create_oci_image(self, file):
        oci_image_layout = {}

    def _configure(self):
        pass

    def _run_scripts(self):
        pass

    def _load_files(self):
        pass
