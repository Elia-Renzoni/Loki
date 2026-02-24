import os
import subprocess
import tarfile
import io
import hashlib
import platform
import shutil
import json
import tempfile
from enum import Enum

from fuseoverlayfs import FuseOverlayFS
from datetime import datetime, timezone
from pathlib import Path

class ImageBuilder:
    _runtime_root_dir = "loki-runtime"
    _runtime_image_manifest = "manifest.json"

    def __init__(self, parsed_cmds):
        self.cmds = parsed_cmds
        self._fs_layers = {}

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
                "x86_64": "alpine-minirootfs-latest-x86_64.tar.gz",
                "i386": "alpine-minirootfs-latest-x86.tar.gz",
                "i686": "alpine-minirootfs-latest-x86.tar.gz",
                "aarch64": "alpine-minirootfs-latest-aarch64.tar.gz",
                "armv7l": "alpine-minirootfs-latest-armv7.tar.gz",
                "armv6l": "alpine-minirootfs-latest-armhf.tar.gz",
            }

            tar_file = supported_archs.get(arch)
            print(tar_file)
            if tar_file is None:
                raise RuntimeError("unsupported CPU architecture")

            return f"https://dl-cdn.alpinelinux.org/alpine/latest-stable/releases/{arch}/{tar_file}"

        rootfs_path = url_composer(platform.machine())
        print(rootfs_path)

        with urllib.request.urlopen(rootfs_path) as resp:
            with tarfile.open(fileobj=io.BytesIO(resp.read()), mode="r:gz") as tar:
                self._safe_extract(tar, target_path)

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
            upperdir=write_only_dir,
            workdir=write_only_dir
        )

        try:
            self._add_layers(None, None, None)

            # execute all the RUN commands
            self._execute(
                self.cmds.get_image_scripts(),
                merge_dir
            )

            snapshot = self._take_filesystem_snapshot(write_only_dir)
            hashed_content = self._do_hash(snapshot)
            self._add_layers(
                    hashed_content,
                    "root_fs",
                    None,
            )

            self._add_layers(None, "history", self.cmds.get_image_scripts())

            # copy source code into the mounted distro
            for target in self.cmds.get_image_copy_targets():
                self._move_source_code(target, write_only_dir)
                snapshot = self._take_filesystem_snapshot(write_only_dir)
                hashed_content = self._do_hash(snapshot)
                self._add_layers(
                        hashed_content, 
                        "root_fs",
                        None,
                )

                self._add_layers(None, "history", self.cmds.get_image_copy_targets())

            # create the assigned workdir
            self._create_workdir(
                self.cmds.get_image_workdir(),
                merge_dir,
            )
            snapshot = self._take_filesystem_snapshot(write_only_dir)
            hashed_content = self._do_hash(snapshot)
            self._add_layers(
                    hashed_content, 
                    "root_fs",
                    None,
            )

            self._add_layers(None, "history", self.cmds.get_image_workdir())

            # transform map
            self._do_flush()
        finally:
            overlayfs.unmount(mnt=merge_dir)  # pyright: ignore[reportCallIssue]

    def _execute(self, commands, merged):
        for cmd in commands:
            if isinstance(cmd, str):
                subprocess.run(
                    cmd,
                    check=True,
                    cwd="/",
                    env={
                        "PATH": "/bin:/usr/bin:/sbin:/usr/sbin",
                        "HOME": "/root",
                        "TERM": "xterm",
                    },
                    preexec_fn=lambda: os.chroot(merged),
                    shell=True,
                )
            else:
                subprocess.run(
                    cmd,
                    check=True,
                    cwd="/",
                    env={
                        "PATH": "/bin:/usr/bin:/sbin:/usr/sbin",
                        "HOME": "/root",
                        "TERM": "xterm",
                    },
                    preexec_fn=lambda: os.chroot(merged),
                )

    def _move_source_code(self, target, workdir):
        dst = os.path.join(workdir, os.path.basename(target))
        shutil.copytree(target, dst, dirs_exist_ok=True)

    def _create_workdir(self, workdir, merged):
        path = Path(merged) / workdir.lstrip("/")
        path.mkdir(parents=True, exist_ok=True)

    def _take_filesystem_snapshot(self, dirty_dir):
        fd, snapshot_path = tempfile.mkstemp(prefix="snapshot-", suffix=".tar.gz")
        os.close(fd)
        with tarfile.open(snapshot_path, "w:gz") as f:
            f.add(dirty_dir, arcname=".")
        return snapshot_path

    def _do_hash(self, snapshot):
        with open(snapshot, "rb") as f:
            digest = hashlib.sha256(f.read()).hexdigest()
        return digest

    class ImageJSONFields(Enum):
        ROOT_FS = "root_fs"
        DIFF_FS = "diff_fs"
        HISTORY= "history"
        TYPE = "type"
        ARCH = "architecture"
        DATE = "created"
        OPERATING_SYSTEM = "os"

    def _add_layers(self, hash_value, layer_id, commands):
        assert layer_id == self.ImageJSONFields.ROOT_FS.value or layer_id is None

        if layer_id == self.ImageJSONFields.ROOT_FS.value:
            if self.ImageJSONFields.ROOT_FS not in self._fs_layers:
                self._fs_layers[self.ImageJSONFields.ROOT_FS] = {}
                self._fs_layers[self.ImageJSONFields.DIFF_FS] = [hash_value]
                self._fs_layers[self.ImageJSONFields.TYPE] = "layer"
            else:
                self._fs_layers[self.ImageJSONFields.DIFF_FS].append(hash_value)

            return

        if layer_id == self.ImageJSONFields.HISTORY.value:
            if self.ImageJSONFields.HISTORY not in self._fs_layers:
                self._fs_layers[self.ImageJSONFields.HISTORY] = []
            else:
                for cmd in commands:
                    entry = {
                            "created": datetime.now(timezone.utc).isoformat(),
                            "created_by": cmd,
                    }
                    self._fs_layers[self.ImageJSONFields.HISTORY].append(entry)
                return

        self._fs_layers[self.ImageJSONFields.DATE] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        self._fs_layers[self.ImageJSONFields.ARCH] = platform.machine()
        self._fs_layers[self.ImageJSONFields.OPERATING_SYSTEM] = "linux"

    def _do_flush(self):
        with open(self._runtime_image_manifest, "w", encoding="utf-8") as f:
            json.dump(self._fs_layers, f)

    def _safe_extract(self, tar, path):
        for member in tar.getmembers():
            member_path = os.path.join(path, member.name)
            if not os.path.realpath(member_path).startswith(os.path.realpath(path) + os.sep):
                raise RuntimeError("tar path traversal detected")
        tar.extractall(path)
