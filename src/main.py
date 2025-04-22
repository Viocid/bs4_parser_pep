import logging
import re
from urllib.parse import urljoin

import requests_cache
from bs4 import BeautifulSoup
from tqdm import tqdm

from collections import defaultdict
from configs import configure_argument_parser, configure_logging
from constants import (BASE_DIR, CODING, EXPECTED_STATUS, MAIN_DOC_URL,
                       PEPS_URL, STATUS, STATUS_ID, STATUS_TABLE)
from outputs import control_output
from utils import find_tag, get_response


def whats_new(session):
    whats_new_url = urljoin(MAIN_DOC_URL, "whatsnew/")
    response = get_response(session, whats_new_url)
    if response is None:
        return
    response.encoding = CODING
    soup = BeautifulSoup(response.text, features="lxml")
    main_div = find_tag(soup, "section", attrs={"id": "what-s-new-in-python"})
    div_with_ul = find_tag(main_div, "div", attrs={"class": "toctree-wrapper"})
    sections_by_python = div_with_ul.find_all(
        "li", attrs={"class": "toctree-l1"}
    )
    results = [("Ссылка на статью", "Заголовок", "Редактор, автор")]
    for section in tqdm(sections_by_python):
        version_a_tag = find_tag(section, "a")
        href = version_a_tag["href"]
        version_link = urljoin(whats_new_url, href)
        response = get_response(session, version_link)
        if response is None:
            continue
        response.encoding = CODING
        soup = BeautifulSoup(response.text, "lxml")
        h1 = find_tag(soup, "h1")
        dl = find_tag(soup, "dl")
        dl_text = dl.text.replace("\n", " ")
        results.append((version_link, h1.text, dl_text))
    return results


def latest_versions(session):
    response = get_response(session, MAIN_DOC_URL)
    if response is None:
        return
    response.encoding = CODING
    soup = BeautifulSoup(response.text, features="lxml")
    sidebar = find_tag(soup, "div", attrs={"class": "sphinxsidebarwrapper"})
    ul_tags = sidebar.find_all("ul")
    for ul in ul_tags:
        if "All versions" in ul.text:
            a_tags = ul.find_all("a")
            break
    else:
        raise Exception("Ничего не нашлось")
    results = [("Ссылка на документацию", "Версия", "Статус")]
    pattern = r"Python (?P<version>\d\.\d+) \((?P<status>.*)\)"
    for a_tag in a_tags:
        link = a_tag["href"]
        match = re.search(pattern, a_tag.text)
        if match:
            version, status = match.groups()
        else:
            version, status = a_tag.text, ""
        results.append((link, version, status))
    return results


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, "download.html")
    response = get_response(session, downloads_url)
    if response is None:
        return
    response.encoding = CODING
    soup = BeautifulSoup(response.text, "lxml")
    table_tag = find_tag(soup, "table", attrs={"class": "docutils"})
    pdf_a4_tag = find_tag(
        table_tag, "a", {"href": re.compile(r".+pdf-a4\.zip$")}
    )
    pdf_a4_link = pdf_a4_tag["href"]
    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split("/")[-1]
    downloads_dir = BASE_DIR / "downloads"
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    response = session.get(archive_url)
    with open(archive_path, "wb") as file:
        file.write(response.content)
    logging.info(f"Архив был загружен и сохранён: {archive_path}")


def pep(session):
    peps_url = urljoin(PEPS_URL, "#pep-status-key")
    response = get_response(session, peps_url)
    if response is None:
        return
    response.encoding = CODING
    soup = BeautifulSoup(response.text, "lxml")
    results = [("Статус", "Колличество")]
    status_counts = defaultdict(int)
    log_messages = []
    rows = soup.select("table.pep-zero-table.docutils.align-default tbody tr")
    for row in tqdm(rows):
        peps_urls = find_tag(row, "a", {"class": "pep reference internal"})
        if not peps_urls:
            continue
        url = urljoin(PEPS_URL, f"{peps_urls['href']}")
        response = get_response(session, url)
        if response is None:
            continue
        response.encoding = CODING
        soup = BeautifulSoup(response.text, "lxml")
        status_codes = find_tag(soup, "abbr")
        if peps_urls['href'] == 'pep-0801/':
            status_counts[status_codes.text] += STATUS
            continue
        status = find_tag(row, "abbr")
        if len(status.text) == STATUS_TABLE and (
            status_codes.text
            in EXPECTED_STATUS[status.text[STATUS_ID]]
        ):
            status_counts[status_codes.text] += STATUS
        elif len(status.text) == STATUS and (
            status_codes.text in EXPECTED_STATUS[""]
        ):
            status_counts[status_codes.text] += STATUS
        elif (
            status_codes.text
            not in EXPECTED_STATUS[status.text[STATUS_ID]]
        ):
            status_counts[status_codes.text] += STATUS
            log_messages.append(
                    f"Несовпадающие статусы: {url} "
                    f"Статус в таблице: {EXPECTED_STATUS.get('', 'N/A')} "
                    f"Статус на странице: {status_codes.text}"
                )
    if log_messages:
        logging.info('\n'.join(log_messages))
    results.extend(sorted(status_counts.items()))
    total = sum(status_counts.values())
    results.append(("Total", total))
    return results


MODE_TO_FUNCTION = {
    "whats-new": whats_new,
    "latest-versions": latest_versions,
    "download": download,
    "pep": pep,
}


def main():
    configure_logging()
    logging.info("Парсер запущен!")
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f"Аргументы командной строки: {args}")
    session = requests_cache.CachedSession()
    if args.clear_cache:
        session.cache.clear()
    parser_mode = args.mode
    results = MODE_TO_FUNCTION[parser_mode](session)
    if results is not None:
        control_output(results, args)
    logging.info("Парсер завершил работу.")


if __name__ == "__main__":
    main()
