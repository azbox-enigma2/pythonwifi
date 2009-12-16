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

tarball:	

changelog:	
	mkdir -p $(TOPDIR)/tmp/
	git log | perl -pi -e 's/</&lt;/g; s/>/&gt;/g; s/@/@<!-- com.com -->/g;' > $(TOPDIR)/tmp/CHANGELOG

clean:
	rm -fr tmp/

distclean:	clean
