#!/usr/bin/env python3

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import tempfile

from pathlib import Path

from wheel.wheelfile import WheelFile


def patch_wheel(src_wheel: Path, dest_dir: Path, patch_dir: Path, suffix: str) -> Path:
    temp_dir = tempfile.mkdtemp()

    try:
        with WheelFile(src_wheel) as w:
            old_dist_info_path = w.dist_info_path
            new_dist_info_path = "{}+{}.dist-info".format(
                w.parsed_filename.group("namever"), suffix
            )
            new_wheel_filename = "{namever}+{suffix}-{pyver}-{abi}-{plat}.whl".format(
                namever=w.parsed_filename.group("namever"),
                suffix=suffix,
                pyver=w.parsed_filename.group("pyver"),
                abi=w.parsed_filename.group("abi"),
                plat=w.parsed_filename.group("plat"),
            )
            new_wheel_path = dest_dir.joinpath(new_wheel_filename)
            print(f"Extracting {src_wheel} to {temp_dir}")
            w.extractall(temp_dir)

        for patch in sorted(os.listdir(patch_dir)):
            patch = patch_dir.absolute().joinpath(patch)
            print(f"Patching with {patch}")
            subprocess.check_call(("patch", "-p1", "-i", str(patch)), cwd=temp_dir)

        os.rename(
            os.path.join(temp_dir, old_dist_info_path),
            os.path.join(temp_dir, new_dist_info_path),
        )

        with WheelFile(new_wheel_path, "w") as w:
            print(f"Repacking wheel as {new_wheel_path}")
            w.write_files(temp_dir)

        return new_wheel_path

    finally:
        # Clean up the temporary directory
        shutil.rmtree(temp_dir)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Patch a Python wheel file")
    parser.add_argument("--wheel", "-w", required=True, help="The wheel file to patch")
    parser.add_argument(
        "--patch-dir",
        "-p",
        required=True,
        help="Directory containing patches to apply",
    )
    parser.add_argument(
        "--dest-dir",
        "-d",
        default=".",
        help="The directory to write the patched wheel to",
    )
    parser.add_argument(
        "--suffix",
        "-s",
        required=True,
        help="The suffix to append to the wheel filename",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    new_wheel_path = patch_wheel(
        Path(args.wheel),
        Path(args.dest_dir),
        Path(args.patch_dir),
        args.suffix,
    )
    print(f"Patched wheel written to {new_wheel_path}")
    return 0


if __name__ == "__main__":
    exit(main())
