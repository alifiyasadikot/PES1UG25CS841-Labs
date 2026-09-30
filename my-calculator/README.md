# my-calculator

A simple Python CLI calculator, built to demonstrate Git version control and a full CI/CD pipeline with GitHub Actions.

## Features

- Core arithmetic: `add`, `subtract`, `multiply`, `divide`, `power`, `square_root` (`sqrt`)
- Command-line interface built with [Click](https://click.palletsprojects.com/)
- Unit tests and integration tests with `pytest`
- Code coverage with `pytest-cov` (80% minimum enforced in CI)
- Static analysis with `pylint` (7.0/10 minimum enforced in CI)
- Formatting with `black`
- Security scanning with `bandit`
- Automated CI/CD pipeline: build → test → coverage → lint → format → security → deploy

## Project structure

```
my-calculator/
├── src/
│   ├── calculator.py     # Core arithmetic functions
│   └── cli.py             # Click-based CLI
├── tests/
│   ├── unit/
│   │   └── test_calculator.py
│   └── integration/
│       └── test_cli_integration.py
├── .github/workflows/
│   └── ci.yml              # CI/CD pipeline
├── requirements.txt
└── pytest.ini
```

## Usage

```bash
pip install -r requirements.txt

python -m src.cli add 5 3
python -m src.cli subtract -- -3 5
python -m src.cli multiply 8 9
python -m src.cli divide 10 3
python -m src.cli power 2 10
python -m src.cli sqrt 16
```

Note: prefix negative numbers with `--` (e.g. `add -- -3 5`) since Click otherwise treats a leading `-` as an option flag.

## Running tests and quality checks locally

```bash
pytest tests/ -v
pytest tests/ --cov=src --cov-report=html

pylint src/

black src/ tests/ --check

bandit -r src/
```

## CI/CD

Every push and pull request triggers the pipeline defined in `.github/workflows/ci.yml`, which runs build, test, coverage, lint, format, and security checks, then packages a deployment artifact.
