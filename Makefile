# Write Math — offline symbol recognizer
#
#   make run     serve the app locally (and on your LAN, e.g. for your phone)
#   make build   assemble the deployable static site in dist/
#   make test    check JS preprocessing + inference against Python
#   make model   retrain the model from scratch (download, prepare, train, export)

PORT    ?= 8000
DIST    ?= dist
PYTHON  ?= python3
VENV    ?= .venv
VPY     := $(VENV)/bin/python
DATA    := training/data


.PHONY: help run build test model clean distclean

help:
	@sed -n 's/^#   //p' $(MAKEFILE_LIST)

# ------------------------------------------------------------------ serving

run:
	@ip=$$(hostname -I 2>/dev/null | awk '{print $$1}'); \
	[ -n "$$ip" ] || ip=$$(ipconfig getifaddr en0 2>/dev/null); \
	echo ""; \
	echo "  Write Math is running:"; \
	echo "    on this computer:  http://localhost:$(PORT)/"; \
	if [ -n "$$ip" ]; then \
	  echo "    on your network:   http://$$ip:$(PORT)/   (open this on your phone; same Wi-Fi)"; \
	  if command -v qrencode >/dev/null; then echo ""; qrencode -t ANSIUTF8 "http://$$ip:$(PORT)/"; fi; \
	fi; \
	echo ""; \
	echo "  Note: over plain http on the network the app works, but offline mode"; \
	echo "  (service worker) needs https:// or localhost. Press Ctrl+C to stop."; \
	echo ""; \
	$(PYTHON) -m http.server --bind 0.0.0.0 --directory docs $(PORT)

# ------------------------------------------------------------------ building

# Copies docs/ to $(DIST)/ and stamps the service worker's cache name with a
# hash of the site's contents, so every deployment with changes is picked up
# by browsers that already have an older version cached.
build: test
	@rm -rf $(DIST)
	@mkdir -p $(DIST)
	@cp -R docs/. $(DIST)/
	@hash=$$(cd docs && find . -type f ! -name sw.js -print0 | sort -z | xargs -0 cat | sha256sum | cut -c1-12); \
	sed -i.bak "s/^const CACHE = \".*\";/const CACHE = \"write-math-$$hash\";/" $(DIST)/sw.js && rm -f $(DIST)/sw.js.bak; \
	echo ""; \
	echo "  Built $(DIST)/ (cache version $$hash):"; \
	(cd $(DIST) && find . -type f | sort | sed 's|^\./|    |'); \
	echo ""; \
	echo "  Copy the contents of $(DIST)/ to any static web server (HTTPS is"; \
	echo "  needed for offline mode). Try it locally with:"; \
	echo "    $(PYTHON) -m http.server --directory $(DIST) $(PORT)"; \
	echo ""

test: docs/model/model.json
	@node tests/parity.mjs

# ------------------------------------------------------------------ training
# Takes about 2-3 hours on a laptop CPU. Needs ~2 GB of disk in training/data.

model: $(VENV)/.installed
	cd training && ../$(VPY) download.py
	cd training && ../$(VPY) prepare.py
	cd training && ../$(VPY) train.py
	cd training && ../$(VPY) export.py
	node tests/parity.mjs

$(VENV)/.installed: training/requirements.txt
	$(PYTHON) -m venv $(VENV)
	$(VPY) -m pip install --quiet --index-url https://download.pytorch.org/whl/cpu torch
	$(VPY) -m pip install --quiet -r training/requirements.txt
	@touch $@

# ------------------------------------------------------------------ cleanup

clean:
	rm -rf $(DIST)

# Also removes the downloaded dataset, intermediate files and the venv.
distclean: clean
	rm -rf $(DATA) $(VENV)
