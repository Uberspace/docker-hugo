#!/bin/sh

main() {
	# set the part of the version to bump (e.g. major, minor, patch)
	local PART="${1:-patch}"
	echo "Updateing '$PART' version…"

	# get next version
	local VERSION=$(
		pipenv run bumpversion --dry-run --verbose "$PART" 2>&1 |
			awk '/^Would tag /{print $3}'
	)
	if [ -z "$VERSION" ]; then
		echo "[ERROR] no version found"
		return 2
	else
		VERSION="${VERSION:1:-1}"
		echo "Prepare Release for: '$VERSION'"
	fi

	# tag the release, so that `reno` finds the recent version
	git tag "$VERSION" || return 3
	# build changelog
	pipenv run reno report --no-show-source --title Changelog --output CHANGELOG.rst
	# remove the tag, we want to include the changes
	git tag -d "$VERSION"
	git add CHANGELOG.rst
	git commit -m ":memo: update CHANGELOG for '$VERSION'"

	# now bump the version for real
	pipenv run bumpversion "$PART"
}

main "$@"
