"""
Assorted utillity tasks…

"""

KEEPFILENAME = '.keep'


def clean(ctx, path, keep=False, **kwargs_keep):
	""" Assert that *path* exists, but remove everything under it. """
	ctx.run(f"mkdir -p '{path}'")
	ctx.run(f"shopt -s dotglob; rm -rf '{path}'/*")
	if keep:
		touch(ctx, path, **kwargs_keep)


def touch(ctx, path, filename=KEEPFILENAME):
	""" Create *filename* in *path*. """
	ctx.run(f"mkdir -p '{path}'")
	ctx.run(f"touch '{path}/{filename}'")
