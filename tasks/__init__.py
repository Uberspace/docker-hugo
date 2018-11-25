"""
Some tasks to help in development.

"""

import pathlib

import invoke

from .utils import docker, misc

BASE_PATH = pathlib.Path(__file__).resolve().parents[1]


@invoke.task
def clean(ctx):
  """ Clean example output. """
  misc.clean(ctx, BASE_PATH / 'example/output')


@invoke.task
def build(ctx, remote=False, tag='', no_cache=False):
  """ Build an image from a Dockerfile. """
  with ctx.cd(str(BASE_PATH)):
    docker.build(ctx, remote=remote, tag=tag, no_cache=no_cache)


@invoke.task(clean)
def run(ctx, remote=False, tag='', command=''):
  """ Run container over mounted `example/`. """
  docker.run(ctx, remote=remote, tag=tag, command=command)


@invoke.task(clean)
def shell(ctx, remote=False, tag=''):
  """ Run a shell in a container from the local image.

  With the directories from `example/` mounted.

  """
  docker.shell(ctx, remote=remote, tag=tag)


@invoke.task
def login(ctx):
  """ Log in to Docker registry. """
  docker.pull(ctx, remote=True)


@invoke.task
def pull(ctx, tag=""):
  """ Pull image from registry. """
  docker.pull(ctx, remote=True, tag=tag)


@invoke.task
def push(ctx, tag=""):
  """ Push image to registry. """
  docker.push(ctx, remote=True, tag=tag)


@invoke.task
def test(ctx, remote=False, tag='', no_cache=False, no_color=False):
  """ Test the results of a previous `run`. """
  color = '--color=never' if no_color else '--color=always'
  build(ctx, remote=remote, tag=tag, no_cache=no_cache)
  run(ctx, remote=remote, tag=tag)
  res = ctx.run(
    f'tree --dirsfirst example/output'
    f' | diff {color} example/expected_output.txt -',
    warn=True,
  )
  if res.ok:
    print('OKAY')
  else:
    raise invoke.exceptions.Exit(message='ERROR', code=1)


@invoke.task()
def release(ctx, tag=""):
  """ Release new image. """
  test(ctx, remote=False, tag=tag, no_cache=True)
  build(ctx, remote=True, no_cache=False)
  push(ctx, tag=tag)


@invoke.task(run)
def server(ctx, port=8080):
  """ Serve the contents of `example/output/` on *port*. """
  with ctx.cd(str(BASE_PATH)):
    misc.serve(ctx.docker.dst, port)


namespace = invoke.Collection()

namespace.configure({
  'docker': {
    'registry': 'registry.uberspace.is',
    'user': '',
    'token': '',
    'namespace': 'uberspace/homepage',
    'name': 'cms-engine',
    'extra': '--user 1000:1000',
    'volumes': {
        '/site': BASE_PATH / 'example/input',
        '/public': BASE_PATH / 'example/output',
    }
  },
  'run': {
    'echo': True,
  },
})

namespace.add_task(build)
namespace.add_task(run)
namespace.add_task(test)

ns_tools = invoke.Collection('tools')
ns_tools.add_task(clean)
ns_tools.add_task(shell)
ns_tools.add_task(server)
ns_tools.add_task(release)
namespace.add_collection(ns_tools)

ns_registry = invoke.Collection('registry')
ns_registry.add_task(login)
ns_registry.add_task(pull)
ns_registry.add_task(push)
namespace.add_collection(ns_registry)
