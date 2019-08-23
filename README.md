# Hugo CMS

**VERSION**: `0.6.0`

This is an [Alpine][] Docker image with the [Hugo][] CMS binary installed.

The Docker tag `latest` always points to the newest image available. To select a
given version of _hugo_, use desired version number as tag, e.g. `0.54.0`.

## :children_crossing: Usage

It's entry point is set to `/usr/local/bin/hugo`. If run, the default command
will run under `root` from `/` with `./site` as input and `../public` as output.

```shell
docker run --rm \
  --volume "$(pwd)/input":/site \
  --volume "$(pwd)/output":/public \
  uberspace/hugo
```

**Note**: you can use `--user $(id -u):$(id -g)` — or similar — to preserve your
file ownership.

## :construction_worker: CI

You could also use the image in the CI for your project, similar to this:

```yaml
hugo:
  stage: build
  image: uberspace/hugo
```

Or use your own entry point:

```yaml
hugo:
  stage: build
  image:
    name: uberspace/hugo
    entrypoint: ['']
  script:
    - /usr/local/bin/hugo --source page --destination /var/www --minify
```

## :bookmark: Release

If you're ready to release a new version, please…

1.  ensure a clean repo (everything merged, release notes ready…),

2.  run the `release` task, from the `release-tools` Docker image to create the
    _CHANGELOG_, _bump the version_ and tag the commits:

    ```shell
    docker run --rm \
    	-v "$(pwd)":/usr/local/src \
    	--user "--user $(id -u):$(id -g)" \
    	uberspace/release-tools release
    ```

3.  and run `git push` and `git push --tags`.

## :rocket: Deployment

Pushes to _master_ trigger builds on [Docker Hub][].

[alpine]: https://hub.docker.com/_/alpine/
[docker hub]: https://hub.docker.com/r/uberspace/hugo
[hugo]: https://gohugo.io
