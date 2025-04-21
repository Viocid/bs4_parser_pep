import csv
import datetime as dt
import logging

from prettytable import PrettyTable

from constants import BASE_DIR, CODING, DATETIME_FORMAT, FIRST, FIRST_EL


def control_output(results, cli_args):
    output = cli_args.output
    if cli_args.mode == "pep":
        file_output(results, cli_args)
    if output == "pretty":
        pretty_output(results)
    elif output == "file":
        file_output(results, cli_args)
    else:
        default_output(results)


def default_output(results):
    for row in results:
        print(*row)


def pretty_output(results):
    table = PrettyTable()
    table.field_names = results[FIRST_EL]
    table.align = "l"
    table.add_rows(results[FIRST:])
    print(table)


def file_output(results, cli_args):
    results_dir = BASE_DIR / "results"
    results_dir.mkdir(exist_ok=True)
    parser_mode = cli_args.mode
    now = dt.datetime.now()
    now_formatted = now.strftime(DATETIME_FORMAT)
    file_name = f"{parser_mode}_{now_formatted}.csv"
    file_path = results_dir / file_name
    with open(file_path, "w", encoding=CODING) as f:
        writer = csv.writer(f, dialect="unix")
        writer.writerows(results)
    logging.info(f"Файл с результатами был сохранён: {file_path}")
