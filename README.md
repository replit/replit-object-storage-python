# replit-storage-python
The library for Replit Object Storage. Development should "just work" on Replit!

## Development

To get setup, run:
```bash
make install
```

To run the linter, run:
```bash
make lint
```

or to fix (fixable) lint issues, run:
```bash
make lint-fix
```

To run tests, run:
```bash
make test
```

## Release

To check that the package builds, you can run:
```bash
make prerelease
```

To perform a release, first bump the version in `pyproject.toml`. Then run:
```bash
make release
```