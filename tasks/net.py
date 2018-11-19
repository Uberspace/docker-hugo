"""
Invoke tasks to serve local contents.

"""

import http.server
import os


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
