# Changes

## 0.3.2026110200

- Reserve send-queue space before posting large replies.
- Wait for reply cleanup when the queue is full, avoiding failed posts and reconnects.

## 0.3.2026110101

- Add `vfs.nfsd.rdma_callback_credits`, defaulting to eight.
- Apply the callback limit to new connections and size their receive reserve.

## 0.3.2026110100

- Reserve receives for callback replies and overlapping reposts.
- Limit callback calls to the peer grant and the local receive reserve.
- Keep the connection open while callback replies make progress.

## 0.3.2026103001

- Retry inline replies when the send pool is full.
- Close the connection if an RDMA error reply cannot obtain a send buffer.

## 0.3.2026103000

- Add a two-digit daily sequence to release versions. Server code is unchanged.

## 0.3.20261030

- Prepare reply allocations before taking the connection mutex.
- Allow RPC framing beyond a 1 MiB READ payload.
- Reuse whole-reply buffers through the existing buffer cache.
- Free temporary reply storage after posting.

## 0.2.20261029

- Use the connection mutex for pending reply chunks and READ boundaries.

## 0.2.20261028

- Reserve one receive buffer outside the forward-call credit grant.
- Use the same credit grant in inline, chunk and error replies.

## 0.2.20261026

- Allow one page of RPC framing beyond a 1 MiB NFS WRITE payload, as
  suggested by Rick Macklem.

## 0.2.20261024

Initial server module and FreeBSD port.

- Register NFS services on each RDMA connection, including after nfsd restarts.
- Preserve the session's backchannel across client reconnects.
- Use a separate mutex for pending reply chunks and read boundaries.
- Log the listener port and address families without verbose boot.
