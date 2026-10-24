# NFS over RDMA server module

This is an unofficial development snapshot. See `SOURCE.json` for the exact
server revision, FreeBSD base and file hashes. Build with the sources for the
kernel that will load the module; the FreeBSD version number alone does not
establish kernel ABI compatibility. This snapshot uses main at
`a3d1d4e88ae7435cfc32a886999dcde2173839cd` (1600029).

The associated port builds and installs `nfsrdma.ko` in `KMODDIR`, normally
`/boot/modules`. It does not enable or reconfigure nfsd. Configure the server
and its RDMA device separately. The client module is a different project.

For a standalone native build:

```
make SRCTOP=/usr/src SYSDIR=/usr/src/sys
```

For a custom kernel, pass its `KERNBUILDDIR` to use its option headers.
Do not load this module into an older kernel merely because compilation
succeeded against a newer source tree.
