# Build and install

Requires FreeBSD 16-CURRENT, a ports tree at `/usr/ports`, and kernel sources
at `/usr/src` that match the running kernel.

## Build the port

```sh
git clone --depth 1 \
    https://github.com/VersatusHPC/freebsd-nfsrdma-kmod.git
cd freebsd-nfsrdma-kmod/port
make SRC_BASE=/usr/src stage check-plist package
```

Install as root:

```sh
make SRC_BASE=/usr/src install
```

### Custom kernels

Set `KERNBUILDDIR` to your kernel's configured object directory:

```sh
make SRC_BASE=/usr/src \
    MAKE_ARGS="SRCTOP=/usr/src KERNBUILDDIR=/path/to/kernel/objects" \
    stage check-plist package
```

Use the same `MAKE_ARGS` when running `make install`. The option headers
must match the running kernel, including `INVARIANTS` and `WITNESS`.

### Offline installation

Download both archives from the
[releases page](https://github.com/VersatusHPC/freebsd-nfsrdma-kmod/releases)
and copy them to `/path/to/downloads` on the FreeBSD host:

- `nfsrdma-kmod-0.3.20261029.tar.gz`: module source.
- `nfsrdma-kmod-port-0.3.20261029.tar.gz`: port recipe and distinfo.

```sh
cd /path/to/downloads
tar -xzf nfsrdma-kmod-port-0.3.20261029.tar.gz
cd nfsrdma-kmod
make DISTDIR=/path/to/downloads SRC_BASE=/usr/src stage check-plist package
```

Install as root:

```sh
make DISTDIR=/path/to/downloads SRC_BASE=/usr/src install
```

## Start the listener

Set up the RDMA interface and NFS exports first. The FreeBSD `nfsd` rc script
must support `nfs_server_rdma_enable` and `nfs_server_rdma_listen`.

Stop nfsd before loading or replacing the module. If an older copy is loaded,
unload it after nfsd stops. Run these commands as root:

```sh
service nfsd stop
kldload /boot/modules/nfsrdma.ko
sysrc nfs_server_rdma_enable=YES
sysrc nfs_server_rdma_listen=20049
service nfsd start
kldstat -m nfsrdma
sysctl vfs.nfsd.rdma_listen
```

The listener logs its port and address families at startup. Check the kernel
log if it fails to start.

The module refuses to unload while nfsd is running. To disable RDMA, stop
nfsd, set `nfs_server_rdma_enable=NO`, unload `nfsrdma`, and restart nfsd.

## Build without ports

From the repository root:

```sh
cd src
make SRCTOP=/usr/src SYSDIR=/usr/src/sys
```

For a custom kernel, also set `KERNBUILDDIR`. This builds without installing.
