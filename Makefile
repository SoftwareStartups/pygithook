INSTALLDIR := $(shell pwd)/install

.PHONY: all test install clean clean_all

default all: install

test: tests
	py.test $<

install:
	INSTALL_BASE=$(INSTALLDIR) ./setup.py install

clean:
	./setup.py clean
	find . -name "*.pyc" |xargs rm -f
	rm -rf obj __pycache__

clean_all: clean
	rm -rf $(INSTALLDIR)
