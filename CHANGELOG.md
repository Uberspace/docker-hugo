# CHANGELOG

## v0.6.2

### Updates

- ⬆️ Update _HUGO_ to `0.82.0`.

## v0.6.1

### Changes

- 🔧 Added default build options: `--cleanDestinationDir`,
  `--i18n-warnings`, `--ignoreCache` and `--verbose`.

## v0.6.0

### Summary

This image is now on [Docker Hub][dh-hugo] as `uberspace/hugo`.

[dh-hugo]: https://hub.docker.com/r/uberspace/hugo

### Changes

- 📦 Moved the repo from internal GitLab to `uberspace/release-tools`.

- 📦 The internal GitLab version now only mirrors the GitHub repo.

### Updates

- ⬆️ Update Hugo to `v0.57.2`.

### Fixes

- 🚀 Add workaround for recent GitLab docker services - see this
  [Issue](https://cdn.knightlab.com/) for more.

## v0.5.2

### Summary

Switch from `pipenv` and a shell script to the `release-tools` Docker image
for handling release related things.

### Changes

- Docs on how to release.

### Removed

- We no longer use `pipenv` for tool dependencies, remove configs for that.

- Remove the shell script to prepare releases.

## v0.5.1

### Added Features

- Added `pipenv` configuration for _development tools_ (`bumpversion` and
  `reno`).

### Updates

- We now document the available _Docker tags_ in the README.

### Fixes

- Fixed the repo URL in the CI example in the README.

## v0.5.0

### Added Features

- Support for configuration directories by _Hugo_.

- Added `git` to the image, to support _git_ stats in _Hugo_.

### Changes

- Generate CHANGELOG with `reno`.

### Updates

- Update _HUGO_ to `0.54.0` (new default version too).

## v0.4.0

### Added Features

- Use _Gitalab CI_ to build the image.

### Removed

- Removed _development tools_ from the repo.

## v0.3.0

### Changes

- Container runs as `root` from `/` over `/site` to `/public`.

### Updates

- Update _development tools_.

### Removed

- Removed links from `/home/hugo/{input,output}` → `/{input,output}`.

- Removed `.gitlab-ci.yaml` for now.

### Known Issues

- Disabled _Gitlab CI_ because of missing Docker runners.

## v0.2.0

### Added Features

- Added TLS **ca-certificates** to image.

## v0.1.0

### Summary

Initial version, pretty much _wip_.
