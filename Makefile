SHELL := /bin/bash
TESTS=$(shell find tests/ -name "*.py")


test:
	nosetests ${TESTS}
