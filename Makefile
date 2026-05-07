VENV := venv
PYTHON := $(VENV)/bin/python
PIP := $(PYTHON) -m pip

.PHONY: venv clean-venv clean-build clean-docs clean docs test build help

help:
	@echo "SmartBinDB build targets:"
	@echo "  make venv        - Create virtual environment and install package"
	@echo "  make clean       - Remove all build/cache files"
	@echo "  make test        - Run test suite"
	@echo "  make docs        - Build Sphinx documentation"
	@echo "  make build       - Build distribution packages"

venv:
	@if [ ! -d "$(VENV)" ]; then \
		python3 -m venv $(VENV); \
		$(PIP) install -U pip wheel setuptools; \
	fi
	$(PIP) install -U -e .

clean-venv:
	rm -rf $(VENV)

clean-build:
	rm -rf *.egg-info build dist .eggs

clean-docs:
	rm -rf docs/build

clean: clean-build clean-docs
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true

test:
	$(PYTHON) -m pytest --cov=smartbindb

docs:
	$(PYTHON) -m pip install -q "sphinx>=7.0" "furo>=2024.1.29" "sphinx-copybutton>=0.5.2"
	sphinx-build -b dirhtml "docs/source" "docs/build/html" -j auto -W --keep-going

build: clean
	$(PYTHON) -m pip install -q build
	$(PYTHON) -m build
