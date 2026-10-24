# Changes

## 0.2.20261024

Initial server module and FreeBSD port.

- Register NFS services on each RDMA connection, including after nfsd restarts.
- Preserve the session's backchannel across client reconnects.
- Use a separate mutex for pending reply chunks and read boundaries.
- Log the listener port and address families without verbose boot.
