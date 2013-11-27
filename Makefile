SHELL := /bin/bash
TESTS=$(shell find tests/ -name "*.py")
VERSION=$(shell python -c "import gachette.lib; print gachette.lib.get_version()")

test:
	nosetests ${TESTS}

version:
	@echo ${VERSION}

release:
	git checkout master
	git fetch upstream
	git pull --rebase upstream master
	python setup.py sdist upload -r pypi && git tag ${VERSION} && git push upstream --tags
