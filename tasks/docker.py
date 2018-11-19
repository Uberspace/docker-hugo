"""
Invoke tasks for handling Docker files and registries.

Configuration
=============

The configuration for all tasks in this module is taken from the context.

A _global_ dictionary is used as a base for the settings, which can be updated
with a _task_ level one. The default name for the _global_ settings dictionary
is `docker`. The name of the current _task_ override, is taken from the value
of the `task` key in the context. If the task level dictionary has set the
`no_global` key to something that evaluates to `True`, the global settings are
ignored.

You can get the current config from the context with :func:`get_config`.

Image Name
----------

:name: name part for the Docker image or container (_required_)
:namespace: _optional_ namespace for the image
:tag: _optional_ tag for the image or container

Options
-------

:src: mount this absolute path at `/input`
:src_to: mountpoint to use instead of `/input`
:dst:  mount this absolute path at `/output`
:dst_to: mountpoint to use instead of `/output`
:shell: use this instead of the default (`/bin/sh`) if interactive
:command: command to use instead of default, when run not interactively
:extra: extra commandline arguments
:no_cache: don't use cache (build only)

Remote Registry
---------------

Registry credentials can be stored in the environment like `INVOKE_DOCKER_USER`
and `INVOKE_DOCKER_TOKEN`.

:remote: use remote Docker registry
:registry: name of the Docker registry (only used if `remote` is set)
:user: username for registry login
:token: token for registry login

Created
-------

:image:  full image name
:container: full conatiner name

"""

import invoke


#  CONFIGURATION

def get_config(ctx, task_key='task', global_key='docker'):
	""" Return configuration namespace for current task from *ctx*.

	Use a global settings dictionary as base and update it with a task level
	one, if present.This uses the *global_key* as name for the base settings and
	takes the key for the local settings from *task_key*, if it exists.

	If the task level dictionary has set the `no_global` key, the global
	settings are ignored.

	"""
	# get base config
	cfg = ctx.get(global_key, {})
	# update with task config
	if task_key in ctx:
		cfg_local = ctx.get(ctx[task_key], {})
		if cfg_local.get('no_global'):
			cfg = cfg_local
		else:
			cfg.update(cfg_local)
	# generated names
	cfg['image'] = get_image_name(cfg)
	cfg['container'] = get_container_name(cfg)
	# return dictionary as Namespace–Object
	return invoke.config.DataProxy.from_data(cfg)


#  IMAGE & CONTAINER

def get_image_name(cfg):
	""" Return full image name (*remote*). """
	tag = cfg.get('tag')
	if cfg.get('remote'):
		tokens = ('registry', 'namespace', 'name')
		if not tag:
			tag = 'master'
	else:
		tokens = ('namespace', 'name')
	image = '/'.join(filter(None, (cfg.get(t) for t in tokens)))
	return f'{image}:{tag}' if tag else image


def get_container_name(cfg):
	""" Return full container name for *job*. """
	container = cfg.get('name')
	tag = cfg.get('tag')
	return f'{container}-{tag}' if tag else container


#  BUILD RUN COMMAND LINE (interactive or not)

def get_run_cmd(ctx, shell=False):
	""" Return command to run image for *job*. """
	cfg = get_config(ctx)
	cmd = ['docker run --rm']
	if shell:
		shell = cfg.get('shell', '/bin/sh')
		cmd.append(f'--interactive --tty --entrypoint {shell}')
	if 'src' in cfg:
		src_to = cfg.get('src_to', '/input')
		cmd.append(
			f"--mount type=bind,source='{cfg.src}',destination={src_to}"
		)
	if 'dst' in cfg:
		dst_to = cfg.get('dst_to', '/output')
		cmd.append(
			f"--mount type=bind,source='{cfg.dst}',destination={dst_to}"
		)
	if 'extra' in cfg:
		cmd.append(cfg.extra)
	cmd.append(f"'{cfg['image']}'")
	if not shell:
		cmd.append(cfg.get('command', ''))
	return ' '.join(cmd).strip()


#  COMMANDS

def build(ctx):
	""" Build  image from Dockerfile. """
	login(ctx)
	cfg = get_config(ctx)
	cmd = ['docker build']
	if cfg.get('no_cache'):
		cmd.append('--no-cache')
	cmd.append(f"--tag '{cfg.image}' .")
	ctx.run(' '.join(cmd))


def shell(ctx):
	""" Run shell in container. """
	login(ctx)
	cmd = get_run_cmd(ctx, shell=True)
	ctx.run(cmd, pty=True)


def run(ctx):
	""" Run container. """
	login(ctx)
	cmd = get_run_cmd(ctx, shell=False)
	ctx.run(cmd)


# REGISTRY

def login(ctx):
	""" Login to docker registry. """
	cfg = get_config(ctx)
	if cfg.get('remote'):
		registry = cfg.get('registry')
		user = cfg.get('user')
		token = cfg.get('token')
		if not all((registry, user, token)):
			raise invoke.exceptions.Exit(message='ERROR: missing credentials', code=1)
		ctx.run(
			f"echo '{token}'"
			f" | docker login --username '{user}' --password-stdin '{cfg.registry}'"
		)


def pull(ctx):
	""" Pull image from registry. """
	login(ctx)
	cfg = get_config(ctx)
	if cfg.get('remote'):
		ctx.run(f"docker pull '{cfg.image}'")


def push(ctx):
	""" Push image to registry. """
	login(ctx)
	cfg = get_config(ctx)
	if cfg.get('remote'):
		ctx.run(f"docker push '{cfg.image}'")
