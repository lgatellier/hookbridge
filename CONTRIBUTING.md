# Contributing

You can contribute to the project in multiple ways:

* Write documentation
* Implement features
* Fix bugs
* Add unit and functional tests
* Everything else you can think of


## Documentation
This project uses :
- [Poetry] for building project :
  - Install poetry : `pip install poetry`
  - Install dependencies : `poetry install`
  - Open a shell in project dédicated virtual env : `poetry shell`
- [Uvicorn] server with live reload for development : `uvicorn --reload hookbridge.main:app`
- [FastAPI] to expose HTTP REST API
- [Dependency Injector] for... dependency injection :wink:

[Poetry]: https://python-poetry.org/
[Uvicorn]: https://www.uvicorn.org/
[FastAPI]: https://fastapi.tiangolo.com
[Dependency Injector]: https://python-dependency-injector.ets-labs.org/


## Development workflow

Before contributing, please make sure you have [pre-commit](https://pre-commit.com)
installed and configured. This will help automate adhering to code style and commit
message guidelines described below:

```shell
  cd webhook-gateway/
  pip3 install --user pre-commit
  pre-commit install -t pre-commit -t commit-msg --install-hooks
```
Please provide your patches as GitHub pull requests. Thanks!


## Commit message guidelines

We enforce commit messages to be formatted using the [conventional-changelog](https://github.com/angular/angular/blob/master/CONTRIBUTING.md#commit).
This leads to more readable messages that are easy to follow when looking through the project history.


## Code-Style

We use black as code formatter, so you'll need to format your changes using the
[black code formatter](https://github.com/python/black). Pre-commit hooks will validate/format your code
when committing. You can then stage any changes `black` added if the commit failed.

To format your code according to our guidelines before committing, run:

```shell
  cd webhook-gateway/
  pip3 install --user black
  black .
```

We also use flake8 to ensure Python's PEP8 best practices are used.
```shell
  cd webhook-gateway/
  pip3 install --user flake8
  flake8 .
```


## Running unit tests

Before submitting a pull request make sure that the tests and lint checks still succeed with
your change. Unit tests run in GitHub Actions and passing checks are mandatory to get
merge requests accepted.

An example can be found in `tests/routes/test_rules.py`

You need to install `tox` (`pip3 install tox`) to run tests locally:

```
# run unit tests for all supported python3 versions :
tox
```
