.PHONY: clean-pyc clean-build test

all: clean sdist wheel

clean: clean-build clean-pyc


clean-build:
	$(info # Removing build artefacts)
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info
	rm -fr .mypy_cache/

clean-pyc:
	$(info # Removing pycies artefacts)
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

isort:
	$(info # Sorting imports)
	sh -c "isort --skip-glob=.tox --recursive . "

lint:
	flake8 --exclude=.tox

dev: dev-requirements.txt
	$(info # Removing pycies artefacts)
	pip install -r dev-requirements.txt


sdist: clean
	$(info # Build the sdist)
	python setup.py sdist
	ls -l dist

wheel: clean
	$(info # Build the wheel)
	python setup.py bdist_wheel
	ls -l dist

pep8:
	autopep8 -aa --in-place --recursive --max-line-length=130 ./src

test:
	$(info # Testing with tox)
	tox
	flake8 ./src/

coverage:
	$(info # Test coverage)
	coverage run --source=./src/ -m py.test tests/ -v --tb=native
	coverage report

coverage-html: coverage
	coverage html

patch:
	bumpversion patch

git-clean:
	git clean -f -d

release: clean
	python setup.py bdist_wheel
	twine upload ./dist/* --verbose

rst: README.md
	pandoc --from=gfm --to=rst --output=README.rst README.md
