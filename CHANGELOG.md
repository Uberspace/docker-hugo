# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project somewhat tries to adhere to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.4] - 2018-12-09

### Added

- Use CI to build image.

### Removed

- Removed development tools from the repo.

## [0.3] - 2018-10-25

### Changed

- Container runs as `root` from `/` over `/site` to `/public`.
- Update development tools.

### Removed

- Removed links from `/home/hugo/{input,output}` → `/{input,output}`
- Removed `.gitlab-ci.yaml` for now.

## [0.2] - 2018-10-22

### Added

- TLS _ca-certificates_.


## 0.1.0 - 2018-10-18

Initial version :tada:

[Unreleased]: https://git.uberspace.is/uberspace/homepage/cms-engine/compare/v0.4.0...HEAD
[0.4]: https://git.uberspace.is/uberspace/homepage/cms-engine/compare/v0.3.0...v0.4.0
[0.3]: https://git.uberspace.is/uberspace/homepage/cms-engine/compare/v0.2.0...v0.3.0
[0.2]: https://git.uberspace.is/uberspace/homepage/cms-engine/compare/v0.1.0...v0.2.0
