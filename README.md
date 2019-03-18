# Hugo CMS

This is an [Alpine][] Docker image with the [Hugo][] CMS installed.

__VERSION__: `0.3.1`

## :children_crossing: Usage

It's entry point is set to `/usr/local/bin/hugo`. If run, the default command
will run under `root` from `/` with `./site` as input and `../public` as output.

```shell
docker run --rm \
  --volume "$(pwd)/example/input":/site \
  --volume "$(pwd)/example/output":/public \
  'registry.uberspace.is/uberspace/homepage/cms-engine'
```

Note: you can use `--user 1000:1000` or similar to preserve your file ownership.

You could also use it in the CI for your project, similar to this:

```yaml
hugo:
    stage: build
    image: registry.uberspace.is/uberspace/homepage/netlify:master
```

Or use your own entry point:

```yaml
hugo:
    stage: build
    image:
        name: registry.uberspace.is/uberspace/homepage/netlify:master
        entrypoint: /usr/local/bin/hugo --source page --destination /var/www --minify
```

## :bookmark: Release

If you're ready to release a new version, please run [bumpversion][] as a last
step:

```shell
pipenv run bumpversion [major|minor|patch]
git push --tags
```

[Alpine]: https://hub.docker.com/_/alpine/
[Hugo]: https://gohugo.io
[bumpversion]: https://github.com/peritus/bumpversion
