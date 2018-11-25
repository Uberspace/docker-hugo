"""
Assorted utillity tasks…

"""

import http.server
import os
import random
import time

import requests

KEEPFILENAME = ".keep"


def clean(ctx, path, keep=False, **kwargs_keep):
    """ Assert that *path* exists, but remove everything under it. """
    with ctx.prefix(f"rm -rf '{path}/'"):
        ctx.run(f"mkdir -p '{path}'")
    if keep:
        touch(ctx, path, **kwargs_keep)


def touch(ctx, path, filename=KEEPFILENAME):
    """ Create *filename* in *path*. """
    with ctx.prefix(f"mkdir -p '{path}'"):
        ctx.run(f"touch '{path}/{filename}'")


def serve(path, port=8080, interface="localhost"):
    """ Serve the contents of *path* on *interface:port*. """
    server_address = (interface, port)
    handler = http.server.SimpleHTTPRequestHandler
    os.chdir(path)
    httpd = http.server.HTTPServer(server_address, handler)
    print(f"Serving '{path}' on 'http://{interface}:{port}/'\n" "CTRL+C to exit…")
    httpd.serve_forever()


def backoff(count):
    """ Return *count* backoff values. """
    if count is 0:
        return [0]
    return (2 ** n + random.randint(0, 1000) / 1000 for n in range(1, count + 1))


def get(url, timeout=6, retries=3):
    """ Return response via _requests_. """
    for seconds in backoff(retries):
        try:
            r = requests.get(url, timeout=timeout)
            r.raise_for_status()
            return r
        except requests.exceptions.RequestException:
            if seconds:
                print(
                    f"Recieving '{url}' failed: {r.reason}. Will retry in {seconds} seconds…"
                )
                time.sleep(seconds)
                continue
            else:
                raise
