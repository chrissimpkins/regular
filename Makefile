build-dev:
	.venv/bin/maturin build

build-release:
	.venv/bin/maturin build --release --strip

build-venv:
	python3 -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r dev-requirements.txt

# installs compiled library in Python venv
install-dev:
	.venv/bin/maturin develop

# installs compiled release target build in Python venv
install-release:
	.venv/bin/maturin develop --release --strip

test: install-dev
	.venv/bin/pytest


.PHONY: build-dev build-release\
install-dev install-release\
test
