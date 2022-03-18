# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = gh-pages
GHPAGESBR     = gh-pages

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

$(BUILDDIR):
	git worktree add $(BUILDDIR) $(GHPAGESBR)

$(BUILDDIR)/.nojekyll: $(BUILDDIR)
	touch $(BUILDDIR)/.nojekyll

.PHONY: worktree
worktree: $(BUILDDIR)/.nojekyll

.PHONY: clean
clean: worktree
	rm -rf $(BUILDDIR)/*

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile worktree
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
