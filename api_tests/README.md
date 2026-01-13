# API Tests Module

## Setup

### Install Dependencies

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running Tests

### Run all API tests

```bash
pytest
```

### Run with specific markers

```bash
pytest -m smoke
pytest -m regression
```

### Run with HTML report

```bash
pytest api_tests/ --html=reports/report.html --self-contained-html
```

### Run in parallel (if pytest-xdist is installed)

```bash
pytest -n auto
```
