import logging
import os
from typing import List, Tuple
import requests
from requests import HTTPError, ConnectionError
from page_loader.known_error import KnownError
from progress.bar import ChargingBar
from page_loader.naming import get_html_file_name
from page_loader.save_page import save_page
from page_loader.parsing import parse_page

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def download(link: str, path: str = os.getcwd()) -> str:
    logger.info(f'Requested url {link}')
    logger.info(f'Output path {path}')
    downloaded_url_name = get_html_file_name(link)
    file_path = os.path.join(path, downloaded_url_name)
    page = download_page(link)
    parsed_page, resources_links = parse_page(page, link, file_path)
    save_page(parsed_page, file_path)
    logger.info('Downloading resources')
    download_resources(resources_links)
    logger.info(f'Webpage was downloaded as {file_path}')
    return file_path


def download_resources(resources_links: List[Tuple[str, str]]) -> None:
    bar = ChargingBar('Downloading resources', max=len(resources_links))
    for resource in resources_links:
        bar.next()
        link, path = resource
        response = requests.get(link)
        try:
            with open(path, 'wb') as f:
                f.write(response.content)
        except OSError as e:
            logger.error(f"Can't open file {path}")
            raise KnownError() from e
    bar.finish()


def download_page(link) -> str:
    response = requests.get(link)
    try:
        response.raise_for_status()
    except (HTTPError, ConnectionError) as error1:
        logger.error(f"Download failed! Status code: {response.status_code}")
        raise KnownError() from error1
    return response.text
