import os
import subprocess
import tarfile
import io
import hashlib
import platform

from fuseoverlayfs import FuseOverlayFS
from datetime import datetime, timezone
from pathlib import Path

class ImageBuilder:
    _runtime_root_dir = "/loki-runtime/"
    _runtime_alpine_rootfs_intel = "https://dl-cdn.alpinelinux.org/alpine/latest-stable/releases/x86_64/alpine-minirootfs-3.19.1-x86_64.tar.gz"
    _runtime_alpine_rootfs_amd = ""
    _runtime_alpine_rootfs_arm = ""
    _runtime_image_manifest = "manifest.json"
    _fs_layers = {}

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

        rootfs_path: str = ""
        match platform.architecture:
            case "ARM":
                rootfs_path = self._runtime_alpine_rootfs_arm
            case "x86_64":
                rootfs_path = self._runtime_alpine_rootfs_intel
            case "amd":
                rootfs_path = self._runtime_alpine_rootfs_amd

        with urllib.request.urlopen(rootfs_path) as resp:
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

        self._add_layers(None, None)

        # execute all the RUN commands
        self._execute(
                self.cmds.get_image_scripts(),
                merge_dir
        )

        snapshot = self._take_filesystem_snapshot(write_only_dir)
        hashed_content = self._do_hash(snapshot)
        self._add_layers(hashed_content, "root_fs")

        # copy source code into the mounted distro
        for target in self.cmds.get_image_copy_targets():
            self._move_source_code(target, write_only_dir)
            snapshot = self._take_filesystem_snapshot(write_only_dir)
            hashed_content = self._do_hash(snapshot)
            self._add_layers(hashed_content, "root_fs")

        # create the assigned workdir
        self._create_workdir(
                self.cmds.get_image_workdir(),
                merge_dir,
        )
        snapshot = self._take_filesystem_snapshot(write_only_dir)
        hashed_content = self._do_hash(snapshot)
        self._add_layers(hashed_content, "root_fs")

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

    def _move_source_code(self, target, upperdir):
        pass

    def _create_workdir(self, workdir, merged):
        path = Path(merged) / workdir.lstrip("/")
        path.mkdir(parents=True, exist_ok=True)

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
        assert layer_id == "root_fs" or layer_id is None

        if layer_id == "root_fs":
            if self._fs_layers["root_fs"] is None:
                self._fs_layers[layer_id] = {}
                self._fs_layers["diff_fs"] = [hash_value]
                self._fs_layers["type"] = "layers"
            else:
                self._fs_layers["diff_fs"] = hash_value

            return

        self._fs_layers["created"] = datetime. now(timezone.utc).isoformat().replace('+00:00', 'Z')

        self._fs_layers["architecture"] = "amd64"
        self._fs_layers["os"] = "linux"
    
