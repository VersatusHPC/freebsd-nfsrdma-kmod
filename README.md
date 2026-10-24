# NFS over RDMA server for FreeBSD

This repository provides a FreeBSD port to run an NFS server over RDMA
using the `nfsrdma.ko` module.

## Requirements

- FreeBSD 16-CURRENT.
- Kernel sources and configuration that match the running kernel.
- An RDMA-capable network adapter with a FreeBSD driver.
- A FreeBSD ports tree.

## Install

Use the [installation instructions](docs/INSTALL.md) to build the port and
enable the RDMA listener. Release archives and checksums are available from
the [releases page](https://github.com/VersatusHPC/freebsd-nfsrdma-kmod/releases).

The port installs the module in `/boot/modules`.

## Development

The module source is in [`src/`](src/), and the port recipe is in [`port/`](port/).

See [changes](CHANGELOG.md) and [contributing](CONTRIBUTING.md).
