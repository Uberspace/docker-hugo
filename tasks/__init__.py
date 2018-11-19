"""
Some tasks to help in development.

"""

import pathlib

import invoke

from . import docker
from . import utils
from . import net


BASE_PATH = pathlib.Path(__file__).resolve().parents[1]


@invoke.task
def clean(ctx):
	""" Clean example output. """
	utils.clean(ctx, ctx.docker.dst)


@invoke.task
def build(ctx, tag='', remote=False, no_cache=False):
	""" Build a local image. """
	ctx['docker']['remote'] = remote
	if tag:
		ctx['docker']['tag'] = tag
	if no_cache:
		ctx['docker']['no_cache'] = True
	with ctx.cd(str(BASE_PATH)):
		docker.build(ctx)


@invoke.task(clean)
def run(ctx, command='', tag='', remote=False):
	""" Run container over mounted `example/`. """
	ctx['docker']['remote'] = remote
	if tag:
		ctx['docker']['tag'] = tag
	if command:
		ctx['docker']['command'] = command
	docker.run(ctx)


@invoke.task(clean)
def shell(ctx, tag='', remote=False):
	""" Run a shell in a container from the local image.

		With the directories from `example/` mounted.

	"""
	ctx['docker']['remote'] = remote
	if tag:
		ctx['docker']['tag'] = tag
	docker.shell(ctx)


@invoke.task
def test(ctx, no_color=False):
	""" Test the results of a previous `run`. """
	color = '--color=never' if no_color else '--color=always'
	res = ctx.run(
		f'tree --dirsfirst example/output'
		f' | diff {color} example/expected_output.txt -'
	)
	if res.ok:
		raise invoke.exceptions.Exit(message='OKAY', code=0)
	else:
		raise invoke.exceptions.Exit(message='ERROR', code=1)


@invoke.task(run)
def server(ctx, port=8080):
	""" Serve the contents of `example/output/` on *port*. """
	net.serve(ctx.docker.dst, port)


@invoke.task
def login(ctx):
	""" Log in to Docker  registry. """
	ctx['docker']['remote'] = True
	docker.login(ctx)


@invoke.task
def pull(ctx, tag=''):
	""" Pull image from registry. """
	ctx['docker']['remote'] = True
	if tag:
		ctx['docker']['tag'] = tag
	docker.pull(ctx)


@invoke.task
def push(ctx, tag=''):
	""" Pull image to registry. """
	ctx['docker']['remote'] = True
	if tag:
		ctx['docker']['tag'] = tag
	docker.push(ctx)


namespace = invoke.Collection()
namespace.configure({
	'docker': {
		'registry': 'registry.uberspace.is',
		'namespace': 'uberspace/homepage',
		'name': 'cms-engine',
		'tag': '',
		'src': BASE_PATH / 'example/input',
		'dst': BASE_PATH / 'example/output',
		'user': '',
		'token': '',
	},
	'run': {
		'echo': True,
	},
})

namespace.add_task(build)
namespace.add_task(run)
namespace.add_task(test)
namespace.add_task(clean)
namespace.add_task(shell)
namespace.add_task(server)

ns_remote = invoke.Collection('remote')
ns_remote.add_task(login)
ns_remote.add_task(pull)
ns_remote.add_task(push)
namespace.add_collection(ns_remote)
