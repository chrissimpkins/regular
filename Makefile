build-dev:
	maturin build

build-release:
	maturin build --release --strip

build-venv:
	python3 -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r dev-requirements.txt

# installs compiled library in Python venv
install-dev:
	maturin develop

# installs compiled release target build in Python venv
install-release:
	maturin develop --release --strip

lint-rust:
	cargo clippy --all-targets --all-features

test: install-dev
	.venv/bin/pytest


.PHONY: build-dev build-release\
install-dev install-release\
test
