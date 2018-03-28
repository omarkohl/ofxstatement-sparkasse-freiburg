PYTHON=.venv/bin/python

all:
	@echo "venv         Set up .venv (dev environment)"
	@echo "clean        Remove .venv"

PYTHON: setup.py clean
	virtualenv -p python3 --no-site-packages .venv
	$(PYTHON) setup.py develop
	.venv/bin/pip install -r requirements_dev.txt

venv: PYTHON

clean:
	rm -rf .venv
