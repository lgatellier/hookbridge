# Webhook router
A configurable webhook router. Routes HTTP webhooks from any source, to any HTTP REST/JSON destination !

This project is currently under development. No stable release is available at the moment.

## Development
1. First, check out sources : `git clone https://github.com/lgatellier/webhook-router`
1. Then, ensure [Poetry] is installed : `python3 -m pip install poetry` 
1. Open a python virtualenv with Poetry : `poetry shell`
1. Install dependencies : `poetry install`
1. Run [Uvicorn] server with live reload : `uvicorn --reload webhook_router.main:app`
1. Have a look to [FastAPI] & [Dependency Injector] documentations
1. You're now ready to contribute !

[Poetry]: https://python-poetry.org/
[Uvicorn]: https://www.uvicorn.org/
[FastAPI]: https://fastapi.tiangolo.com
[Dependency Injector]: https://python-dependency-injector.ets-labs.org/

## Testing

This project uses tox to run unit tests. Simply run `tox` in project root directory !