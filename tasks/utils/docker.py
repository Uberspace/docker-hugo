"""
Invoke tasks for handling Docker files and registries.

Functions
=========

You can call the following functions:

- `build`
- `shell`
- `run`
- `login`
- `pull`
- `push`

With this signature::

  func(ctx, use_cfg=None, **cfg_overrides)

If *use_cfg* is not set, the configuration is taken from the global value
(default: `docker`), that needs to be available from the context.
*cfg_overrides* are optional and can be used to overide any of the setting
described below (or see :data:`CONFIGUTATION_KEYS`).

Configuration
=============

The configuration for all tasks in this module is taken from the context.

Image Name
----------

:name: name part for the Docker image or container (_required_)
:namespace: _optional_ namespace for the image
:tag: _optional_ tag for the image or container

Options
-------

:volumes: A dictonary, where the keys are mount points in the containerand the
  values paths on the host (or volume names, if they don't start with a `/`).
:envvars: A dictionary of environment variables names to set in the container,
  for `None` values, the value is taken from the current environment.
:extra: extra commandline arguments
:shell: use this instead of the default (`/bin/sh`) (shell only)
:command: command to use instead of default (run only)
:context: use this build context (default '.', build only)
:buildargs: use these (build only)
:no_cache: don't use the build cache (build only)

Remote Registry
---------------

Registry credentials can be stored in the config, or in the environment, like
`INVOKE_DOCKER_USER` and `INVOKE_DOCKER_TOKEN` (or `INVOKE_TASKNAME_USER`…).

:remote: use remote Docker registry (default: `False`)
:registry: name of the Docker registry (only used if `remote` is set)
:user: username for registry login
:token: token for registry login

Created
-------

:image:  full image name
:container: full conatiner name

"""

import invoke

from . import cfg


class DockerConfig(cfg.TaskConfig):

  GLOBAL_KEY = "docker"

  LOCAL_KEY_NAME = "local_config_key"

  OVERRIDE_KEYS = [
    "buildargs",
    "command",
    "container",
    "context",
    "envvars",
    "extra",
    "image",
    "name",
    "namespace",
    "no_cache",
    "registry",
    "remote",
    "shell",
    "tag",
    "token",
    "user",
    "volumes",
  ]

  AUTO_SETTINGS = {
    'image': 'get_image_name',
    'container': 'get_container_name',
  }

  def get_image_name(self, cfg):
    """ Return full image name. """
    tag = cfg.get("tag")
    if cfg.get("remote"):
      tokens = ("registry", "namespace", "name")
      if not tag:
        tag = "master"
    else:
      tokens = ("namespace", "name")
    image = "/".join(filter(None, (cfg.get(t) for t in tokens)))
    image = f"{image}:{tag}" if tag else image
    return image

  def get_container_name(self, cfg):
    """ Return full container name. """
    container = cfg.get("name")
    tag = cfg.get("tag")
    container = f"{container}-{tag}" if tag else container
    return container


config = DockerConfig()


def get_cmd_build(cfg):
  """ Return "build" command. """
  cmd = ["docker build"]

  if cfg.get("no_cache"):
    cmd.append("--no-cache")

  for key, value in cfg.get("buildargs", {}).items():
    cmd.append(f"--build-arg '{key}={value}'")

  bctx = cfg.get("context", ".")
  cmd.append(f"--tag '{cfg.image}' '{bctx}'")

  cmd = " ".join(cmd)
  return cmd


def get_cmd_run(cfg, interactive=False):
  """ Return "run" command. """
  cmd = ["docker run --rm"]

  for mount_point, path in cfg.get("volumes", {}).items():
    cmd.append(f"--volume '{path}':'{mount_point}'")

  for key, value in cfg.get("envvars", {}).items():
    if value is None:
      cmd.append(f"--env '{key.upper()}'")
    else:
      cmd.append(f"--env '{key.upper()}={value}'")

  if "extra" in cfg:
    cmd.append(cfg.extra)

  if interactive:
    shell = cfg.get("shell", "/bin/sh")
    cmd.append(f"--interactive --tty --entrypoint '{shell}'")

  cmd.append(f"'{cfg.image}'")

  if not interactive and "command" in cfg:
    cmd.append(cfg.command)

  cmd = " ".join(cmd)
  return cmd


def get_cmd_login(cfg):
  """ Return tuple of "login" command and needed environment. """
  try:
    registry = cfg["registry"]
    user = cfg["user"]
    token = cfg["token"]
  except KeyError:
    raise invoke.exceptions.Exit(message="ERROR: missing credentials", code=1)

  cmd = f'docker login --username "$USER"  --password "$TOKEN" \'{registry}\''
  env = {"USER": user, "TOKEN": token}
  return (cmd, env)


def get_cmd_pull(cfg):
  """ Return "pull" command. """
  return f"docker pull '{cfg.image}'"


def get_cmd_push(cfg):
  """ Return "pull" command. """
  return f"docker push '{cfg.image}'"


@cfg.with_config(config)
def build(ctx, cfg):
  """ Build  image from Dockerfile. """
  cmd = get_cmd_build(cfg)
  ctx.run(cmd)


@cfg.with_config(config)
def shell(ctx, cfg):
  """ Run shell in container. """
  pull(ctx)
  cmd = get_cmd_run(cfg, interactive=True)
  ctx.run(cmd, pty=True)


@cfg.with_config(config)
def run(ctx, cfg):
  """ Run container. """
  pull(ctx)
  cmd = get_cmd_run(cfg, interactive=False)
  ctx.run(cmd)


@cfg.with_config(config)
def login(ctx, cfg):
  """ Login to docker registry. """
  if cfg.get("remote"):
      (cmd, env) = get_cmd_login(cfg)
      ctx.run(cmd, env=env)


@cfg.with_config(config)
def pull(ctx, cfg):
    """ Pull image from registry. """
    if cfg.get("remote"):
        login(ctx)
        cmd = get_cmd_pull(cfg)
        ctx.run(cmd)


@cfg.with_config(config)
def push(ctx, cfg):
    """ Push image to registry. """
    if cfg.get("remote"):
        login(ctx)
        cmd = get_cmd_push(cfg)
        ctx.run(cmd)
