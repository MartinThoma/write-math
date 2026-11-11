#!/usr/bin/env bash
# Print the GitHub Pages URL of a remote's repository.
# Usage: scripts/pages-url.sh [remote]
set -euo pipefail
slug=$(git remote get-url "${1:-origin}" | sed -E 's#^(git@|ssh://git@|https://)github\.com[:/]##; s#\.git$##')
owner=$(printf '%s' "${slug%%/*}" | tr '[:upper:]' '[:lower:]')
repo=${slug#*/}
echo "  Site: http://$owner.github.io/$repo/  (GitHub Pages updates within a minute or two)"
