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

#### Additional options

##### Filename prefix

An environment variable named `NMRE_JUNIT_PREFIX` can be defined with a value to be prefixed onto the file name. Note that no separator is used so you may want to include one.

```shell
export NMRE_JUNIT_BASE=test-results
export NMRE_JUNIT_PREFIX="report-"
pytest [...]

# after either example, a file named something like
# `test-results/report-1735941218.338192.xml` will be created
```

##### Filename suffix types

An environment variable named `NMRE_JUNIT_SUFFIX_TYPE` can be defined to control what type of suffix is used. Valid values are `timestamp` (default), `uuid4`, and `uuid7`.

```shell
export NMRE_JUNIT_BASE=test-results
export NMRE_JUNIT_PREFIX="report-"
export NMRE_JUNIT_SUFFIX_TYPE=uuid4
pytest [...]

# after either example, a file named something like
# `test-results/report-ffe95fcc-b818-4aca-a350-e0a35b9de6ec.xml` will be created
```

### Adding testsuite/testcase properties

The plugin adds two optional CLI flags, `--testsuite-property` and `--testcase-property`, which provide a means to adding properties to the testsuite and testcase JUnit elements respectively.

Both flags accept multiple arguments and use the same format: `name=value`. Each passed argument is split on the _first_ `=` character, so any additional characters in an individual arg will be part of the value. For example, `opts=gpu=h100` would result in a property with name `opts` and value `gpu=h100`.

> [!NOTE]
> Arguments passed to the `--testcase-property` flag will be added as properties to _all_ test cases in the run.

> [!IMPORTANT]
> Because these flags accept multiple arguments, they must be added **after** any positional args. It is okay to include them before other flags.

#### Example: Adding testsuite properties

```shell
pytest [...] --testsuite-property gpu=h100
# adds a property to the testsuite element with name 'gpu' and value 'h100'
pytest [...] --testsuite-property gpu_name=h100 gpu_count=2
# adds two properties to the testsuite element: one with name=gpu_name/value=h100
# and one with name=gpu_count/value=2
```

#### Example: Adding testcase properties

```shell
pytest [...] --testcase-property gpu=h100
# adds a property to all testcase elements with name 'gpu' and value 'h100'
pytest [...] --testcase-property gpu_name=h100 gpu_count=2
# adds two properties to all testcase elements: one with
# name=gpu_name/value=h100 and one with name=gpu_count/value=2
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
