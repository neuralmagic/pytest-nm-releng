# pytest-nm-releng

A pytest plugin offering various functionality for Neural Magic’s Release Engineering team.

## Installation

The Python package can be installed directly from this git repository from either a branch or tag:

```shell
# recommended: use a version tag (e.g., v0.2.0)
pip install https://github.com/neuralmagic/pytest-nm-releng/archive/v0.2.0.tar.gz

# alternative: install based on a branch (e.g., main)
pip install https://github.com/neuralmagic/pytest-nm-releng/archive/main.tar.gz
```

## Features

### Dynamically-named JUnit report files

`pytest-nm-releng` can automatically generate unique, dynamically-named JUnit report files with an optional prefix. The report file is generated when the test run begins using Python’s `datetime.timestamp()` method (UTC).

> [!NOTE]
> This works by appending the `--junit-xml` flag after the command is run, meaning it will override any previously-specified instances of this flag.

To enable this behavior, define the environment variable `NMRE_JUNIT_BASE` with a value to the path where the test files should be stored. This can be absolute or relative.

The following examples will both write JUnit report files in a folder named "test-results" in the current working directory.

```shell
# example: prefixing a command
NMRE_JUNIT_BASE=test-results pytest [...]

# example: export the environment variable (useful if pytest is not being
# invoked directly)
export NMRE_JUNIT_BASE=test-results
pytest [...]

# after either example, a file named something like
# `test-results/1735941024.348248.xml` will be created
```

Optionally, you can define `NMRE_JUNIT_PREFIX` with a value to be prefixed onto the file name. Note that no separator is used so you may want to include one.

```shell
export NMRE_JUNIT_BASE=test-results
export NMRE_JUNIT_PREFIX="report-"
pytest [...]

# after either example, a file named something like
# `test-results/report-1735941218.338192.xml` will be created
```

## Contributing

To contribute, follow these general steps:

1. Fork the repository

1. Create a new branch

1. Make your changes

1. Install `tox`

   ```shell
   # example: using pipx
   pipx install tox
   # example: using uv
   uv tool install tox --with tox-uv
   ```

1. Run quality checks and tests

   ```shell
   # apply available automatic style/formatting fixes
   tox -e format
   # check style/formatting
   tox -e style
   # run tests
   tox -e py
   ```

1. Submit a pull request with your changes

## Acknowledgements

This pytest plugin was generated with [Cookiecutter] along with [@hackebrot]'s [cookiecutter-pytest-plugin] template.

[@hackebrot]: https://github.com/hackebrot
[cookiecutter]: https://github.com/audreyr/cookiecutter
[cookiecutter-pytest-plugin]: https://github.com/pytest-dev/cookiecutter-pytest-plugin
