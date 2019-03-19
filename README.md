# Hugo CMS

This is an [Alpine][] Docker image with the [Hugo][] CMS binary installed.

**VERSION**: `0.5.1`

The Docker tag `latest` always points to the newest image available. To select a
given version of _hugo_, use desired version number as tag, e.g. `0.54.0`.

## :children_crossing: Usage

It's entry point is set to `/usr/local/bin/hugo`. If run, the default command
will run under `root` from `/` with `./site` as input and `../public` as output.

```shell
docker run --rm \
  --volume "$(pwd)/example/input":/site \
  --volume "$(pwd)/example/output":/public \
  'registry.uberspace.is/uberspace/homepage/hugo'
```

Note: you can use `--user $(id -u):$(id -g)` — or similar — to preserve your
file ownership.

Note: you need to use `docker login registry.uberspace.is`, before you can
access the registry. You can create a **deploy token** with read access to the
registry for that in the [registry settings][].

## :construction_worker: CI

You could also use it the image in the CI for your project, similar to this:

```yaml
hugo:
  stage: build
  image: registry.uberspace.is/uberspace/homepage/hugo
```

Or use your own entry point:

```yaml
hugo:
  stage: build
  image:
    name: registry.uberspace.is/uberspace/homepage/hugo
    entrypoint: [""]
  script:
    - /usr/local/bin/hugo --source page --destination /var/www --minify
```

## :bookmark: Release

If you're ready to release a new version, please run:

1. `pipenv sync` to setup the needed environment,
2. ensure a clean repo (everything merged, release notes ready…)
3. run `./prepare_release.sh` to create the _CHANGELOG_, _bump the version_
   and tag the commits.
4. run `git push` and `git push --tags`.

[alpine]: https://hub.docker.com/_/alpine/
[hugo]: https://gohugo.io
[bumpversion]: https://github.com/peritus/bumpversion
[registry settings]: https://git.uberspace.is/uberspace/homepage/hugo/settings/repository
