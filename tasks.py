"""
Some tasks to help in development.

"""

import http.server
import os

import invoke


def get_image_name(ctx):
    """ Return full image name from context. """
    return f"{ctx.docker.namespace}{ctx.docker.image}"


@invoke.task
def clean(ctx):
    """ Clean example output. """
    ctx.run('rm -rf example/output')
    ctx.run('mkdir -p example/output')


@invoke.task
def build(ctx, cache=True):
    """ Build local image. """
    image = get_image_name(ctx)
    cache = '' if cache else '--no-cache'
    ctx.run(f"docker build {cache} --tag '{image}' .")


@invoke.task(build, clean)
def shell(ctx):
    """ Run a shell in the local image. """
    image = get_image_name(ctx)
    ctx.run(
        (
            f"docker run --rm --interactive --tty --entrypoint /bin/sh"
            f' --mount type=bind,src="$(pwd)/example/input",dst=/input'
            f' --mount type=bind,src="$(pwd)/example/output",dst=/output'
            f" '{image}'"
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
    image = get_image_name(ctx)
    ctx.run(
        (
            f"docker run --rm"
            f' --mount type=bind,src="$(pwd)/example/input",dst=/input,readonly'
            f' --mount type=bind,src="$(pwd)/example/output",dst=/output'
            f" '{image}' {command}"
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
def server(ctx, port=8080):
    """ Serve the contents of `example/output/` on *port*. """
    server_address = ('', port)
    handler = http.server.SimpleHTTPRequestHandler
    os.chdir('example/output')
    httpd = http.server.HTTPServer(server_address, handler)
    print(f'Serving example on port {port}\nCTRL+C to exit…')
    httpd.serve_forever()


namespace = invoke.Collection()
namespace.configure({
    'docker': {
        'namespace': 'uberspace/homepage/',
        'image': 'cms-engine',
    },
    'run': {
        'echo': True,
    },
})

namespace.add_task(build)
namespace.add_task(clean)
namespace.add_task(run)
namespace.add_task(server)
namespace.add_task(shell)
namespace.add_task(test)
