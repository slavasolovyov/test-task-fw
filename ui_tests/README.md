# UI Tests Module

## Setup

### Install Dependencies

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running Tests

### Run all UI tests

```bash
pytest
```

### Run with specific browser

Tests run on both Chrome and Firefox by default. To run on specific browser:

```bash
pytest -k "chrome"

pytest -k "firefox"
```

### Run with markers

```bash
pytest  -m regression
pytest  -m smoke
```

### Run with Allure report

```bash
pytest 

allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report
```
