# Hugo CMS

This is the docker image for the homepage's CMS engine build on [Hugo][].

It can build the static files for the homepage.

__VERSION__: `0.2.1`

## Usage

Run this image with your _input_ and _output_ paths mounted:

- It runs over all input files mounted at `/input`.
- And writes the results to whatever is mounted at `/output`.

```shell
docker run --rm \
  --mount type=bind,source="$(pwd)/example/input",destination=/input \
  --mount type=bind,source="$(pwd)/example/output",destination=/output \
  'registry.uberspace.is/uberspace/homepage/cms-engine'
```

## Development

If you're ready to release a new version run:

```shell
pipenv run bumpversion [major|minor|patch]
git push --tags
```

[Hugo]: https://gohugo.io
