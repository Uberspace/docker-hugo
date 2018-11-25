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
ENTRYPOINT [ "/usr/local/bin/hugo" ]
CMD [ "--source", "./site", "--destination", "../public", "--minify"]
