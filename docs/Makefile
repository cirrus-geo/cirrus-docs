HTTP_PORT = 8000
EXTRA     = extra
SOURCEDIR = src
BUILDDIR = _build
SPHINXOPTS    +=
SPHINXBUILD   ?= sphinx-build
PLUGIN_VERSION ?= $(shell git rev-parse --abbrev-ref HEAD) 

gh-pages:
	git worktree add gh-pages gh-pages

gh-pages/.nojekyll: gh-pages
	touch $@

gh-pages/index.html: gh-pages/.nojekyll $(EXTRA)/index.html
	cp $(EXTRA)/index.html $@

gh-pages/$(PLUGIN_VERSION):
	mkdir $@

.PHONY: gh-pages-clean
gh-pages-clean:
	rm -rf gh-pages/$(PLUGIN_VERSION)

.PHONY: gh-pages-copy
gh-pages-copy: gh-pages-clean gh-pages/$(PLUGIN_VERSION)
	cp -r $(BUILDDIR)/html/* gh-pages/$(PLUGIN_VERSION)

.PHONY:
gh-pages-versions-update: gh-pages
	python3 update-versions.py gh-pages

.PHONY: gh-pages-update
gh-pages-update: clean build gh-pages/index.html gh-pages-copy gh-pages-versions-update

.PHONY: clean
clean:
	rm -rf $(BUILDDIR)

.PHONY: build
build: html

.PHONY: serve
serve: gh-pages
	python -m http.server $(HTTP_PORT) -d gh-pages 

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%:
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
