# Hugo CMS

This is an [Alpine][] Docker image with the [Hugo][] CMS binary installed.

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
    entrypoint: [""]
  script:
    - /usr/local/bin/hugo --source page --destination /var/www --minify
```

## :rocket: Deployment

Pushes to _main_ trigger builds on [Docker Hub][].

[alpine]: https://hub.docker.com/_/alpine/
[docker hub]: https://hub.docker.com/r/uberspace/hugo
[hugo]: https://gohugo.io
