import os
import subprocess
import tarfile
import io
import hashlib
import platform
import shutil
import json
from enum import Enum

from fuseoverlayfs import FuseOverlayFS
from datetime import datetime, timezone
from pathlib import Path

class ImageBuilder:
    _runtime_root_dir = "/loki-runtime/"
    _runtime_alpine_rootfs_base_url = "https://dl-cdn.alpinelinux.org/alpine/latest-stable/releases/"
    _runtime_alpine_rootfs_x86 = "https://dl-cdn.alpinelinux.org/alpine/latest-stable/releases/x86_64/alpine-minirootfs-3.19.1-x86_64.tar.gz"
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

        def url_composer(arch):
            supported_archs = {
                "x86_64": "alpine-minirootfs-3.20.0-x86_64.tar.gz",
                "i386": "alpine-minirootfs-3.20.0-x86.tar.gz",
                "i686": "alpine-minirootfs-3.20.0-x86.tar.gz",
                "aarch64": "alpine-minirootfs-3.20.0-aarch64.tar.gz",
                "armv7l": "alpine-minirootfs-3.20.0-armv7.tar.gz",
                "armv6l": "alpine-minirootfs-3.20.0-armhf.tar.gz",
            }

            tar_file = supported_archs[arch]
            if tar_file is None:
                raise RuntimeError("unsopported CPU architecture")

            return f"https://dl-cdn.alpinelinux.org/alpine/latest-stable/releases/{arch}/{tar_file}"

        try:
            rootfs_path = url_composer(platform.machine())
        except Exception as e:
           raise e

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
        

        # transorm map
        self._do_flush()

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

    def _move_source_code(self, target, workdir):
        shutil.copytree(target, workdir)

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

    class ImageJSONFields(Enum):
        ROOT_FS = "root_fs"
        DIFF_FS = "diff_fs"
        TYPE = "type"
        ARCH = "architecture"
        DATE = "created"
        OPERATING_SYSTEM = "os"

    def _add_layers(self, hash_value, layer_id):
        assert layer_id == self.ImageJSONFields.ROOT_FS or layer_id is None

        if layer_id == self.ImageJSONFields.ROOT_FS:
            if self._fs_layers[self.ImageJSONFields.ROOT_FS] is None:
                self._fs_layers[layer_id] = {}
                self._fs_layers[self.ImageJSONFields.DIFF_FS] = [hash_value]
                self._fs_layers[self.ImageJSONFields.TYPE] = "layer"
            else:
                self._fs_layers[self.ImageJSONFields.DIFF_FS] = hash_value

            return

        self._fs_layers[self.ImageJSONFields.DATE] = datetime. now(timezone.utc).isoformat().replace('+00:00', 'Z')
        self._fs_layers[self.ImageJSONFields.ARCH] = platform.architecture
        self._fs_layers[self.ImageJSONFields.OPERATING_SYSTEM] = "linux"

    def _do_flush(self):
        json.dumps(self._fs_layers)
    
