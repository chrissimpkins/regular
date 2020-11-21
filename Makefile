# installs compiled library in Python venv
develop:
	maturin develop

# installs compiled release target build in Python venv
develop-rel:
	maturin develop --release --strip


.PHONY: develop develop-rel