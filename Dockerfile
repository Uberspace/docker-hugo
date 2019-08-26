FROM alpine AS build
ARG HUGO_VERSION=0.57.2
RUN apk add --no-cache curl
WORKDIR /tmp
RUN set -ex \
    && base_url='https://github.com/gohugoio/hugo/releases/download' \
    && path="v${HUGO_VERSION}/hugo_${HUGO_VERSION}_Linux-64bit.tar.gz" \
    && curl --location "$base_url/$path" | tar --extract --gzip \
    && ./hugo version

FROM alpine
RUN apk add --update --no-cache ca-certificates git
COPY --from=build /tmp/hugo /usr/local/bin/
ENTRYPOINT [ "/usr/local/bin/hugo" ]
CMD [ \
	"--source", "./site", \
	"--destination", "../public", \
	"--cleanDestinationDir", \
	"--i18n-warnings", \
	"--ignoreCache", \
	"--minify", \
	"--verbose" \
]
