"""
Deal with multiple levels of configuration based on the current context.

"""

import functools
import logging

import invoke


def with_config(configurator):
  """ Setup configuration with *configurator* and pass it along. """
  def _outer(func):

    @functools.wraps(func)
    def _wrapper(ctx, **kwargs):
      (cfg, func_kwargs) = configurator(ctx.config.clone(), **kwargs)
      result = func(ctx, cfg, **func_kwargs)
      return result

    return _wrapper
  return _outer


class TaskConfig:

  """
  Handle multiple configuation levels.

  1. A __global__ dictionary is used as a base for the settings. It is taken
     from a given key in the context (`GLOBAL_KEY`).

  2. This can be updated with __local__ settings. Taken from another dict in the
     context, identified by the value of the `LOCAL_KEY_NAME`.

  3. If the local level dictionary has set the `no_global_config` key to
     something, that evaluates to `True`, the global settings are ignored,
     otherwise they are updated with the local settings.

  4. If __overrides__ exists, they are applied. Allowed overrides are listed in
     `OVERRIDE_KEYS`.

  5. Function can populate the config with computed values (see
     `AUTO_SETTINGS`).

  Needs at least a `global_key` for setup. Set `ctx` to feed it with data
  afterwards.

  """

  GLOBAL_KEY = None

  LOCAL_KEY_NAME = None

  OVERRIDE_KEYS = None

  AUTO_SETTINGS = {}

  OPTIONS = {
    'no_global_key': 'no_global_config',
    'overrides_filter_true': True,
    'use_auto_settings': True,
  }

  def __init__(
    self, global_key=None, local_key_name=None, override_keys=None,
    auto_settings=None, options=None
  ):
    self.global_key = global_key or self.GLOBAL_KEY
    self.local_key_name = local_key_name or self.LOCAL_KEY_NAME
    self.override_keys = override_keys or self.OVERRIDE_KEYS or []
    self.auto_settings = auto_settings or self.AUTO_SETTINGS or {}
    self.options = options or self.OPTIONS.copy()
    self.ctx = {}
    if self.global_key is None:
      raise ValueError('at least the global key needs to be set')

  @property
  def global_config(self):
    """ Return global configuration. """
    return self.ctx.get(self.global_key, {})

  @property
  def local_key(self):
    """ Return the current key for local settings."""
    if self.local_key_name is None:
      return None
    return self.ctx.get(self.local_key_name)

  @local_key.setter
  def local_key(self, key):
    """ Set key for current local settings. """
    if self.local_key_name is None:
      raise NotImplementedError('This config does not support local settings.')
    self.ctx[self.local_key_name] = key

  @property
  def local_config(self):
    """ Return local configuration. """
    local_key = self.local_key
    if local_key is None:
      return {}
    return self.ctx.get(local_key, {})

  def filter_overrides(self, kwargs):
    """ Return a tuple of overrides and leftovers from *kwargs*. """
    overrides = {}
    leftovers = {}
    for key, value in kwargs.items():
      if key in self.override_keys:
        overrides[key] = value
      else:
        leftovers[key] = value
    return (overrides, leftovers)

  def merge_config(self, **kwargs):
    """ Return tuple of merged configurations and leftover *kwargs*. """
    logging.debug(f"Kwargs: {kwargs}")
    cfg_global = self.global_config
    logging.debug(f"Global: {cfg_global}")

    cfg_local = self.local_config
    logging.debug(f"Local: {cfg_local}")

    (overrides, leftovers) = self.filter_overrides(kwargs)
    logging.debug(f"Overrides: {overrides}")
    if self.options['overrides_filter_true']:
      overrides = {k: v for k, v in overrides.items() if v}
    logging.debug(f"Overrides (filtered): {overrides}")
    logging.debug(f"Leftovers: {leftovers}")

    if cfg_local:
      if cfg_local.get(self.options['no_global_key']):
        cfg = cfg_local.copy()
      else:
        cfg = cfg_global.copy()
        cfg.update(cfg_local)
    else:
      cfg = cfg_global.copy()
    cfg.update(overrides)
    logging.debug(f"CONFIG: {cfg}")

    if self.options['use_auto_settings']:
      auto_settings = {
        name: getattr(self, func)(cfg)
        for name, func in self.auto_settings.items()
      }
      logging.debug(f"AUTO: {auto_settings}")
      cfg.update(auto_settings)

    cfg = invoke.config.DataProxy.from_data(cfg)
    return (cfg, leftovers)

  def __call__(self, ctx, **kwargs):
    """ Return tuple of configuration from *ctx* and leftovers from *kwargs*. """
    self.ctx = ctx
    return self.merge_config(**kwargs)
