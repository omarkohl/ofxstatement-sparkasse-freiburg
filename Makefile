VENV_NAME=.venv
PYTHON=$(VENV_NAME)/bin/python

all:
	@echo "clean        Remove virtualenv"
	@echo "test         Execute tests"
	@echo "venv         Set up dev environment"

PYTHON: setup.py
	virtualenv -p python3 --no-site-packages $(VENV_NAME)
	$(PYTHON) setup.py develop
	$(VENV_NAME)/bin/pip install -r requirements_dev.txt

venv: PYTHON

clean:
	rm -rf $(VENV_NAME)

test: PYTHON
	$(VENV_NAME)/bin/pytest \
		--ofxstatement-bin=$(VENV_NAME)/bin/ofxstatement \
		tests
