FROM alpine AS build
ARG HUGO_VERSION=0.49.2
RUN apk add --no-cache curl
WORKDIR /tmp
RUN set -ex \
    && url="https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_${HUGO_VERSION}_Linux-64bit.tar.gz" \
    && curl --location "$url" | tar --extract --gzip \
    && ./hugo version

FROM alpine
RUN apk add --update --no-cache ca-certificates
COPY --from=build /tmp/hugo /usr/local/bin/
RUN set -ex \
    && addgroup -g 1000 hugo \
    && adduser -u 1000 -G hugo -D hugo \
    && mkdir /input /output \
    && chown hugo:hugo /input /output
USER hugo:hugo
WORKDIR /home/hugo
ENTRYPOINT [ \
    "/usr/local/bin/hugo", \
    "--source", "/input", \
    "--destination", "/output", \
    "--minify" \
]
CMD []
