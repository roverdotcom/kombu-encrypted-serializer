.PHONY: clean
clean: clean-build clean-pyc


.PHONY: clean-build
clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info


.PHONY: clean-pyc
clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +


.PHNONY: release
release: clean
	python setup.py sdist upload
	python setup.py bdist_wheel upload


.PHNONY: dist
dist: clean
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist


.PHONY: test
test:
	docker build \
		--progress plain \
		--target test \
		--build-arg RUN_ID=$(shell date +%s) \
		.


.DEFAULT_GOAL := test
