#!/usr/bin/env bash
# Publish a built static site directory to the gh-pages branch of a remote,
# without touching the current checkout. Each deploy is one commit on top of
# the remote gh-pages branch; nothing is pushed if the site is unchanged.
#
# Usage: scripts/publish-gh-pages.sh <site-dir> [remote] [branch]
set -euo pipefail

site=${1:?usage: $0 <site-dir> [remote] [branch]}
remote=${2:-origin}
branch=${3:-gh-pages}

[ -f "$site/index.html" ] || { echo "error: $site/index.html not found (run make build)" >&2; exit 1; }

# Build the tree in a throw-away index so the working tree and the real index stay untouched.
export GIT_INDEX_FILE
GIT_INDEX_FILE=$(mktemp -d)/index
trap 'rm -rf "$(dirname "$GIT_INDEX_FILE")"' EXIT
git --work-tree="$site" add --all --force .
tree=$(git write-tree)

parent=""
if git fetch --quiet "$remote" "refs/heads/$branch" 2>/dev/null; then
  parent=$(git rev-parse FETCH_HEAD)
  if [ "$(git rev-parse "$parent^{tree}")" = "$tree" ]; then
    echo "$remote/$branch is already up to date."
    exit 0
  fi
fi

source_rev=$(git rev-parse --short HEAD)
git diff --quiet HEAD -- || source_rev="$source_rev+uncommitted changes"
commit=$(git commit-tree "$tree" ${parent:+-p "$parent"} \
  -m "Deploy $(git rev-parse --abbrev-ref HEAD) @ $source_rev")

git push "$remote" "$commit:refs/heads/$branch"
echo "Pushed $commit to $remote/$branch."
