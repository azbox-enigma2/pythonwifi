#
# Makefile for Python WiFi
#

SHELL = /bin/sh

package 	= python-wifi

srcdir = .

VERSION = $(shell cat $(srcdir)/docs/VERSION)

BRANCH = "master"

TOPDIR := $(CURDIR)

.PHONY: all egg tarball changelog clean distclean

all:	

egg:	
	python setup.py bdist_egg

tarball: $(TOPDIR)/tmp/${package}-$(VERSION).tar.bz2.sign $(TOPDIR)/tmp/${package}-$(VERSION).tar.bz2.sha256

$(TOPDIR)/tmp/${package}-$(VERSION).tar.bz2.sign: $(TOPDIR)/tmp/${package}-$(VERSION).tar.bz2
	cd $(TOPDIR)/tmp && gpg --detach-sign -a --output ${package}-$(VERSION).tar.bz2.asc ${package}-$(VERSION).tar.bz2
	cd $(TOPDIR)/tmp && chmod 644 ${package}-$(VERSION).tar.bz2.asc
	cd $(TOPDIR)/tmp && gpg --verify ${package}-$(VERSION).tar.bz2.asc

$(TOPDIR)/tmp/${package}-$(VERSION).tar.bz2.sha256:
	cd $(TOPDIR)/tmp && sha256sum ${package}-$(VERSION).tar.bz2 > ${package}-$(VERSION).tar.bz2.sha256

$(TOPDIR)/tmp/${package}-$(VERSION).tar.bz2:
	rm -fr $(TOPDIR)/tmp
	mkdir -p $(TOPDIR)/tmp/
	git archive --format=tar --prefix=${package}-$(VERSION)/ $(BRANCH) | (cd $(TOPDIR)/tmp/ && tar xf -)
	find $(TOPDIR)/tmp/${package}-$(VERSION) -type f -exec chmod ug+r  {} \;
	find $(TOPDIR)/tmp/${package}-$(VERSION) -type d -exec chmod ug+rx {} \;
	chmod 755 $(TOPDIR)/tmp/${package}-$(VERSION)/examples/iw*.py
	cd $(TOPDIR)/tmp && tar -ch ${package}-$(VERSION) | bzip2 > ${package}-$(VERSION).tar.bz2
	cd $(TOPDIR)/tmp && chmod 644 ${package}-$(VERSION).tar.bz2
	ls -l $(TOPDIR)/tmp/

changelog:	
	mkdir -p $(TOPDIR)/tmp/
	git log | perl -pi -e 's/</&lt;/g; s/>/&gt;/g; s/@/@<!-- com.com -->/g;' > $(TOPDIR)/tmp/CHANGELOG

clean:
	rm -fr tmp/

distclean:	clean
