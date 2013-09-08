SHELL := /bin/bash
TESTS=$(shell find tests/ -name "*.py")
VERSION=$(shell python -c "import gachette; print gachette.get_version()")

test:
	nosetests ${TESTS}

version:
	@echo ${VERSION}

release:
	python setup.py sdist upload -r pypi
	git tag ${VERSION}
	git push upstream --tags
