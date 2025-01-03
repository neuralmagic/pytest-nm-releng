# pytest-nm-releng

A pytest plugin offering various functionality for Neural Magic’s Release Engineering team.

## Contributing

To contribute, follow these general steps:

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Install `tox`
    ```shell
    # example: using pipx
    pipx install tox
    # example: using uv
    uv tool install tox --with tox-uv
    ```
5. Run quality checks and tests
    ```shell
    # apply available automatic style/formatting fixes
    tox -e format
    # check style/formatting
    tox -e style
    # run tests
    tox -e py
    ```
6. Submit a pull request with your changes


## Acknowledgements

This pytest plugin was generated with [Cookiecutter] along with [@hackebrot]'s [cookiecutter-pytest-plugin] template.

[@hackebrot]: https://github.com/hackebrot
[cookiecutter]: https://github.com/audreyr/cookiecutter
[cookiecutter-pytest-plugin]: https://github.com/pytest-dev/cookiecutter-pytest-plugin
