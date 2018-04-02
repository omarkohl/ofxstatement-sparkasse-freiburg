SHELL=/bin/bash

VENV_NAME=.venv
PYTHON=$(VENV_NAME)/bin/python

all:
	@echo "clean        Remove virtualenv"
	@echo "package      Create a .tar.gz Python package"
	@echo "test         Execute tests"
	@echo "venv         Set up dev environment"

PYTHON: setup.py
	virtualenv -p python3 --no-site-packages $(VENV_NAME)
	$(PYTHON) setup.py develop
	$(VENV_NAME)/bin/pip install -r requirements_dev.txt

venv: PYTHON

clean:
	rm -rf $(VENV_NAME)
	rm -rf dist/
	rm -rf .pytest_cache/
	find . -type d -name __pycache__ -exec rm -rf {} \;
	find . -type d -name "*.egg-info" -exec rm -rf {} \;

test: PYTHON
	$(VENV_NAME)/bin/pytest \
		--ofxstatement-bin=$(VENV_NAME)/bin/ofxstatement \
		tests

package: PYTHON
	$(PYTHON) setup.py sdist
