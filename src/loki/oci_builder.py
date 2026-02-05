import os
import subprocess

from fuseoverlayfs import FuseOverlayFS

class ImageBuilder:
    _runtime_root_dir = "/loki-runtime/"
    _runtime_alpine_rootfs = "https://dl-cdn.alpinelinux.org/alpine/latest-stable/releases/x86_64/alpine-minirootfs-3.19.1-x86_64.tar.gz"
    _runtime_image_manifest = "manifest.json"
    _fs_layers = {}
    _std_oci_spec = []

    def __init__(self, parsed_cmds):
        self.cmds = parsed_cmds

    def run(self):
        self._init_workspace()

    def _init_workspace(self):
        image_name = self.cmds.get_image_name()
        if image_name is None:
            pass
        target_path = os.path.join(self._runtime_root_dir, image_name)
        os.makedirs(target_path, exist_ok=True)

        # install alpine rootfs
        import urllib.request
        import tarfile
        import io

        with urllib.request.urlopen(self._runtime_alpine_rootfs) as resp:
            with tarfile.open(fileobj=io.BytesIO(resp.read()), mode="r:gz") as tar:
                tar.extractall(target_path)

        self._build_image(target_path)

    def _build_image(self, parent):
        merge_dir = os.path.join(parent, "merge")
        lower_dir = os.path.join(parent, "lower")
        worker_dir = os.path.join(parent, "worker")
        dirs = [merge_dir, lower_dir, worker_dir]
        for d in dirs:
            os.makedirs(d, exist_ok=True)

        overlayfs = FuseOverlayFS.init()
        overlayfs.mount(  # pyright: ignore[reportCallIssue]
            mnt=merge_dir,
            lowerdirs=lower_dir,
            upperdir=parent,
            workdir=worker_dir
        )

        self._fork_exec(
                self.cmds.get_image_scripts(),
                merge_dir
        )

        self._fork_exec(
                self.cmds.get_image_copy_targets(),
                merge_dir
        )


        self._fork_exec(
                self.cmds.get_image_workdirs(),
                merge_dir
        )

    def _fork_exec(self, commands, merged):
        subprocess.run(
           commands,
           check=True,
           cwd="/",
           env={
                "PATH": "/bin:/usr/bin:/sbin:/usr/sbin",
                "HOME": "/root",
                "TERM": "xterm",
            },
            preexec_fn=lambda: os.chroot(merged)
        )

    def _checksum(self):
        pass

