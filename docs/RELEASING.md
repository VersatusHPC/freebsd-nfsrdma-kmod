# Prepare a release

Source changes need a new version. Update:

- `release.json`: version and timestamp.
- `src/SOURCE.json`: version, source revision, FreeBSD base and file hashes.
- `port/Makefile`: `DISTVERSION`.

Keep the exporter and template hashes from the original export unless you
import the source again. Update `CHANGELOG.md` and the archive filenames in
`docs/INSTALL.md`.

## Build the archives

Use an output directory that does not already exist:

```sh
python3 tools/release.py --output dist/release
cp dist/release/distinfo port/distinfo
python3 tools/release.py --check
```

This creates the source and port archives, `SHA256`, and `distinfo`.

Build and package the port on the target FreeBSD kernel. Install it, load
the module, and run the RDMA regression tests before publishing.

## Publish

Commit the release files and create a matching `vVERSION` tag. Upload both
archives and `SHA256` to the GitHub release. Mark it as a prerelease until
acceptance tests pass.

Download the uploaded archives and compare them with the local `SHA256`.
For a public release, also check downloads without authentication and confirm
that the port fetches its source archive.

Do not replace published source archives. Changes belong in a new release.
Publish source and port archives only; binary packages depend on the kernel.
