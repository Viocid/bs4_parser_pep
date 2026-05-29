# PEP Parser

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup4-parsing-green)
![Requests](https://img.shields.io/badge/Requests-HTTP-orange)
![Pytest](https://img.shields.io/badge/Pytest-tested-green)

Command-line parser for Python documentation and PEP status analytics.

The project collects data from official Python documentation pages, parses HTML with BeautifulSoup and outputs results as tables or CSV files.

---

## Main features

- Parse Python "What's New" pages
- Collect latest Python versions and statuses
- Download Python documentation archive
- Parse PEP pages and calculate status statistics
- Compare PEP statuses from the index and individual pages
- Save results to CSV files
- Pretty table output in terminal
- Request caching
- Rotating file logging
- CLI arguments with `argparse`
- Automated tests with Pytest

---

## Tech stack

- Python
- BeautifulSoup4
- Requests
- Requests Cache
- LXML
- PrettyTable
- TQDM
- Pytest
- Flake8

---

## Project structure

```text
bs4_parser_pep/
├── src/
│   ├── configs.py          # CLI and logging configuration
│   ├── constants.py        # URLs, constants and settings
│   ├── exceptions.py       # Custom exceptions
│   ├── main.py             # Parser modes and entry point
│   ├── outputs.py          # Table and file output logic
│   ├── utils.py            # Request and HTML helper functions
│   └── results/            # Generated CSV reports
├── tests/                  # Automated tests
├── pytest.ini
├── .flake8
└── requirements.txt
```

---

## Parser modes

| Mode | Description |
|---|---|
| `whats-new` | Parses Python release notes pages |
| `latest-versions` | Collects Python documentation versions and statuses |
| `download` | Downloads Python documentation archive |
| `pep` | Parses PEP pages and calculates status statistics |

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Viocid/bs4_parser_pep.git
cd bs4_parser_pep
```

Create and activate virtual environment:

```bash
python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

General command format:

```bash
python src/main.py <mode> [options]
```

Available options:

| Option | Description |
|---|---|
| `-c`, `--clear-cache` | Clear request cache before running |
| `-o pretty` | Print result as a formatted table |
| `-o file` | Save result to CSV file |

---

## Examples

Parse Python release notes:

```bash
python src/main.py whats-new -o pretty
```

Get latest Python versions:

```bash
python src/main.py latest-versions -o file
```

Download documentation archive:

```bash
python src/main.py download
```

Analyze PEP statuses:

```bash
python src/main.py pep -o file
```

---

## Output

The parser can output data in two formats:

- formatted terminal table;
- CSV file in the `results/` directory.

Logs are written to:

```text
src/logs/parser.log
```

---

## Running tests

```bash
pytest
```

---

## What this project demonstrates

- Web scraping with BeautifulSoup
- Working with external documentation resources
- CLI application design
- Request caching
- CSV report generation
- Logging with rotating file handler
- Error handling for missing HTML elements
- Automated testing
