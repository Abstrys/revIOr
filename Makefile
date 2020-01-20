# makefile for revIOr

install:
	./setup.py install --user

clean:
	./setup.py clean --all

spotless:
	rm -rf build dist revIOr.egg-info

dist: spotless
	./setup.py build sdist

upload: build
	twine upload dist/*
