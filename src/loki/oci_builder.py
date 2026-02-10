import os
import subprocess
import tarfile
import io
import hashlib

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

        with urllib.request.urlopen(self._runtime_alpine_rootfs) as resp:
            with tarfile.open(fileobj=io.BytesIO(resp.read()), mode="r:gz") as tar:
                tar.extractall(target_path)

        self._build_image(target_path)

    def _build_image(self, parent):
        merge_dir = os.path.join(parent, "merge")
        read_only_dir = os.path.join(parent, "lower")
        write_only_dir = os.path.join(parent, "upper")
        dirs = [merge_dir, read_only_dir, write_only_dir]
        for d in dirs:
            os.makedirs(d, exist_ok=True)

        # virtual filesystem creation
        overlayfs = FuseOverlayFS.init()
        overlayfs.mount(  # pyright: ignore[reportCallIssue]
            mnt=merge_dir,
            lowerdirs=read_only_dir,
            upperdir=parent,
            workdir=write_only_dir
        )

        # execute all the RUN commands
        self._execute(
                self.cmds.get_image_scripts(),
                merge_dir
        )

        snapshot = self._take_filesystem_snapshot(write_only_dir)
        hashed_content = self._do_hash(snapshot)

    def _execute(self, commands, merged):
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

    def _take_filesystem_snapshot(self, dirty_dir):
        snaphost = "snaphost.tar"
        with tarfile.open(snaphost, "w:gz") as f:
            f.add(dirty_dir, arcname=".")
        return snaphost

    def _do_hash(self, snapshot):
        digest = None
        with open(snapshot, "rb") as f:
            digest = hashlib.sha256(f.read()).hexdigest()
        return digest
            

    def _add_layers(self, hash_value, layer_id):
       layout = {}

