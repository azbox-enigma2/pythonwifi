#
# Makefile for Python WiFi
#

SHELL = /bin/sh

package 	= python-wifi

VERSION = $(shell cat $(srcdir)/docs/VERSION)

TOPDIR := $(CURDIR)

.PHONY: all egg tarball changelog clean distclean

all:	

egg:	

tarball:	

changelog:	
	mkdir -p $(TOPDIR)/tmp/
	git log | perl -pi -e 's/</&lt;/g; s/>/&gt;/g; s/@/@<!-- com.com -->/g;' > $(TOPDIR)/tmp/CHANGELOG

clean:
	rm -fr tmp/

distclean:	clean
