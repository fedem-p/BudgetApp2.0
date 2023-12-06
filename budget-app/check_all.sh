echo "============= Linting =================="
poetry run isort --profile black .

poetry run black .

poetry run pylint *.py

poetry run pylint ./**/*.py

echo "============= Testing =================="
poetry run pytest --cov