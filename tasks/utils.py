"""
Assorted utillity tasks…

"""

import http.server
import os


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


def serve(path, port=8080, interface='localhost'):
	""" Serve the contents of *path* on *interface:port*. """
	server_address = (interface, port)
	handler = http.server.SimpleHTTPRequestHandler
	os.chdir(path)
	httpd = http.server.HTTPServer(server_address, handler)
	print(
		f"Serving '{path}' on 'http://{interface}:{port}/'\n"
		"CTRL+C to exit…"
	)
	httpd.serve_forever()
