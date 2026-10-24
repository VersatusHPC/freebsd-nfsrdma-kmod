#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-2-Clause
"""Check release metadata or produce deterministic source and port archives."""

import argparse
import gzip
import hashlib
import io
import json
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def archive(root: str, entries: dict[str, bytes], timestamp: int) -> bytes:
    stream = io.BytesIO()
    with (
        gzip.GzipFile(fileobj=stream, mode="wb", filename="",
                      compresslevel=6, mtime=timestamp) as gz,
        tarfile.open(fileobj=gz, mode="w", format=tarfile.USTAR_FORMAT) as tar,
    ):
        for name, data in sorted(entries.items()):
            info = tarfile.TarInfo(f"{root}/{name}")
            info.size = len(data)
            info.mode = 0o644
            info.mtime = timestamp
            tar.addfile(info, io.BytesIO(data))
    return stream.getvalue()


def prepare() -> tuple[dict[str, bytes], dict[str, bytes]]:
    release = json.loads((ROOT / "release.json").read_text())
    version, timestamp = release["version"], release["timestamp"]
    manifest_bytes = (ROOT / "src/SOURCE.json").read_bytes()
    manifest = json.loads(manifest_bytes)
    if manifest["version"] != version:
        raise ValueError("source manifest version differs from release.json")
    files = {}
    for name, expected in manifest["files"].items():
        relative = Path(name)
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError(f"invalid source path: {name}")
        data = (ROOT / "src" / relative).read_bytes()
        if digest(data) != expected:
            raise ValueError(f"source hash differs: {name}")
        files[name] = data
    files["SOURCE.json"] = manifest_bytes
    source_name = f"nfsrdma-kmod-{version}.tar.gz"
    source_archive = archive(f"nfsrdma-kmod-{version}", files, timestamp)
    port = {name: (ROOT / "port" / name).read_bytes()
            for name in ("Makefile", "pkg-descr")}
    if f"DISTVERSION=\t{version}\n".encode() not in port["Makefile"]:
        raise ValueError("port version differs from release.json")
    master_site = (
        b"MASTER_SITES=\thttps://github.com/VersatusHPC/"
        b"freebsd-nfsrdma-kmod/releases/download/v${DISTVERSION}/\n"
    )
    if master_site not in port["Makefile"]:
        raise ValueError("port does not use the versioned release location")
    port["distinfo"] = (
        f"TIMESTAMP = {timestamp}\n"
        f"SHA256 ({source_name}) = {digest(source_archive)}\n"
        f"SIZE ({source_name}) = {len(source_archive)}\n"
    ).encode()
    artifacts = {
        source_name: source_archive,
        f"nfsrdma-kmod-port-{version}.tar.gz": archive("nfsrdma-kmod", port, timestamp),
    }
    return artifacts, port


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        artifacts, port = prepare()
        checksums = "".join(f"{digest(data)}  {name}\n"
                            for name, data in sorted(artifacts.items()))
        if args.check:
            if port["distinfo"] != (ROOT / "port/distinfo").read_bytes():
                raise ValueError("port/distinfo differs from the source archive")
            print("Source manifest and port metadata match.")
        else:
            args.output.mkdir(parents=True, exist_ok=False)
            for name, data in artifacts.items():
                (args.output / name).write_bytes(data)
            (args.output / "SHA256").write_text(checksums)
            (args.output / "distinfo").write_bytes(port["distinfo"])
        print(checksums, end="")
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(1, f"release check failed: {error}\n")


if __name__ == "__main__":
    main()
