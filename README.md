# Budget APP

[![Linting](https://github.com/fedem-p/BudgetApp2.0/actions/workflows/linting.yml/badge.svg)](https://github.com/fedem-p/BudgetApp2.0)
[![Tests](https://github.com/fedem-p/BudgetApp2.0/actions/workflows/testing.yml/badge.svg)](https://github.com/fedem-p/BudgetApp2.0)

a simple app to track expenses and incomes.

## Detting started

To run the app you'll need to have `poetry` installed:

```bash
pip install poetry
```

then you can use poetry to install all the dependencies and to run any command:

```bash
cd budget-app   # you need to be in the same folder as poetry.lock and pyproject.toml
poetry install
```

Finally, you can try running the app:

```bash
poetry run python app.py
```

## Tests

To run the tests you can use poetry again:

```bash
poetry run pytest -s
```

## Linting

You can lint the code running `black`, `isort` and `pylint`:

```bash
poetry run black .

poetry run isort --profile black .

poetry run pylint $(git ls-files '*.py')
```

## Development

Current state:

Most of the app code is in the `app.py` and `data_manager.py` files.

`app.py` contains the UI and all the UI functionality, plus some core app functionality.
Once it's almost all there, it will be important to separate each component in modules (UI modules for each page) or more.

Inside `data_manager.py` there's the core module to handle the data.
The data is stored in 2 files and structured like this:

`data.csv` is a list of all transaction in the following format:

| date       | type   | amount | account | category | subcategory | note |
| ---------- | ------ | ------ | ------- | -------- | ----------- | ---- |
| 2018-01-03 | income | 94.0   | N26     | salary   | evotec      | may  |

`metadata.json` contains other information: account names, categories and subcategories

In the future there may eb an extra file to store statistics and avoid computing them all the time.

## Maybe in the future

Build the docker file:

```docker build -t my-budget-image .```

where `python-dev latest` is a custom image with ubuntu and python installed.

and then run the container:

```docker run -it -v /home/fpuppo/workspace/budget-app/budget-app:/app my-budget-image```

attach vs code to the container and start developing!
