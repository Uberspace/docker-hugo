"""
Some tasks to help in development.

"""

import http.server
import os

import invoke


@invoke.task
def clean(ctx):
    """ Clean example output. """
    ctx.run('rm -rf example/output')
    ctx.run('mkdir -p example/output')


@invoke.task
def build(ctx, cache=True):
    """ Build local image. """
    cache = '' if cache else '--no-cache'
    ctx.run(f"docker build {cache} --tag '{ctx.namespace}{ctx.image_name}' .")


@invoke.task(build)
def shell(ctx):
    """ Run a shell in the local image. """
    ctx.run(
        (
            f"docker run --rm --interactive --tty --entrypoint /bin/sh"
            f' --mount type=bind,src="$(pwd)/example/input",dst=/input'
            f' --mount type=bind,src="$(pwd)/example/output",dst=/output'
            f" '{ctx.namespace}{ctx.image_name}'"
        ),
        pty=True,
    )


@invoke.task(
    pre=[build, clean],
    help={
        'command': "HUGO command to run",
    },
)
def run(ctx, command=''):
    """ Run container from image with `example/` mounted.

        You can set a HUGO command to run and / or options trough *command*,
        e.g. `--buildDrafts`, `--buildExpired` or `--buildFuture`.

    """
    ctx.run(
        (
            f"docker run --rm"
            f' --mount type=bind,src="$(pwd)/example/input",dst=/input,readonly'
            f' --mount type=bind,src="$(pwd)/example/output",dst=/output'
            f" '{ctx.namespace}{ctx.image_name}' {command}"
        )
    )


@invoke.task(run)
def test(ctx, color=True):
    """ Test the results of running the build for the example. """
    color = '--color=always' if color else ''
    res = ctx.run(
        f'tree --dirsfirst example/output'
        f' | diff {color} - example/expected_output.txt'
    )
    if res.ok:
        raise invoke.exceptions.Exit(message='OKAY', code=0)
    else:
        raise invoke.exceptions.Exit(message='ERROR', code=1)


@invoke.task(run)
def serve(ctx, port=8080):
    """ Serve the contents of `example/output/` on *port*. """
    server_address = ('', port)
    handler = http.server.SimpleHTTPRequestHandler
    os.chdir('example/output')
    httpd = http.server.HTTPServer(server_address, handler)
    print(f'Serving example on port {port}\nCTRL+C to exit…')
    httpd.serve_forever()


namespace = invoke.Collection()
namespace.configure({
    'namespace': 'uberspace/homepage/',
    'image_name': 'cms-engine',
    'run': {
        'echo': True,
    },
})

namespace.add_task(build)
namespace.add_task(clean)
namespace.add_task(run)
namespace.add_task(serve)
namespace.add_task(shell)
namespace.add_task(test)
