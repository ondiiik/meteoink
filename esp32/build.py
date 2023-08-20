#!/usr/bin/python3
import glob
import os
import struct
import zlib
import git
from pathlib import Path


root = Path(os.getcwd()).resolve()


class Builder:
    def __init__(self, dst, variant):
        self.cwd = root.joinpath("..", "micropython").resolve()
        self.dwd = root.joinpath(dst, variant).resolve()
        print(self.cwd, "->", self.dwd)
        self.fw = root.joinpath("meteoink.fw")
        self.mpc = str(root.joinpath("mpy-cross")) + " -v -march=xtensawin"
        self.repo = git.Repo(search_parent_directories=True)
        self.variant = variant

    def __call__(self, cleanup=False):
        try:
            self.build_cleanup(cleanup)
            self.build_copy()
            self.build_check()
        finally:
            self.command(f"cd {root}")

    def build_cleanup(self, cleanup):
        if cleanup:
            self.command(f"rm -Rf {self.dwd}")

        self.command(f"mkdir {self.dwd}")

    def build_copy(self):
        self.copy("www")

        if self.variant == "acep":
            self.copy("bitmaps/acep/wind.bin")
            self.copy("bitmaps/acep/fonts.bin")
            self.copy("bitmaps/acep/bmp.bin")
        elif self.variant == "gs":
            self.copy("bitmaps/gs/fonts.bin")
            self.copy("bitmaps/gs/bmp.bin")
        else:
            with open(f"{self.dwd}/bitmaps", "w"):
                ...

    def build_check(self):
        l = list(self.dwd.rglob("*"))

        for item in self.dwd.rglob("*"):
            if item.is_file():
                # File exceeding this size make cause troubles with littlefs
                if item.stat().st_size > 524288:
                    print(
                        f"\n[!!! WARNING !!!] TOO BIG FILE - {item} :: {item.stat().st_size}"
                    )

    def command(self, cmd, variant=None):
        if variant is not None and variant != self.variant:
            return

        print(cmd)
        os.system(cmd)

    def copy(self, p):
        src = Path(self.cwd, p)
        dst = Path(self.dwd, p)
        cmd = (
            f"rm -Rf {dst}",
            f"mkdir -p {dst if src.is_dir() else dst.parent}",
            f'rsync -avL --exclude="__pycache__" "{src}/." "{dst}/."'
            if src.is_dir()
            else f'cp "{src}" "{dst}"',
        )

        for c in cmd:
            self.command(c)


builder_bwy = Builder("micropython", "bwy")
builder_bwy(cleanup=True)

builder_acep = Builder("micropython", "acep")
builder_acep(cleanup=True)

builder_acep = Builder("micropython", "gs")
builder_acep(cleanup=True)
