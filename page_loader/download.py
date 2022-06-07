import logging
import os
import requests
from urllib.parse import urlparse, urljoin

from requests import HTTPError, ConnectionError

from page_loader.known_error import KnownError
from progress.bar import ChargingBar
from bs4 import BeautifulSoup
from page_loader.supporting_functions import get_name, get_dir_name, get_content, get_html_file, \
    get_resource_full_name, get_response

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


tags = {'link': 'href',
        'img': 'src',
        'script': 'src'}


def download(link: str, path: str = os.getcwd()) -> str:
    logger.info(f'Requested url {link}')
    logger.info(f'Output path {path}')
    try:
        os.makedirs(path, exist_ok=True)
    except PermissionError as e:
        logger.error(f"Can't create directory {path}. Invalid path")
        raise KnownError() from e
    except FileNotFoundError as err:
        logger.error(f"Not exists path {path}")
        raise KnownError() from err
    downloaded_url_name = get_html_file(link)
    file_path = os.path.join(path, downloaded_url_name)
    response = get_response(link)
    try:
        response.raise_for_status()
        with open(file_path, 'wb') as f:
            f.write(response.content)
    except (HTTPError, ConnectionError) as error1:
        logger.error(f"Download failed! Status code: {response.status_code}")
        raise KnownError() from error1
    except OSError as error2:
        logger.error(f"Can't open file {file_path}")
        raise KnownError() from error2
    download_data(link, file_path)
    logger.info(f'Webpage was downloaded as {file_path}')
    return file_path


def download_data(link: str, file_path: str) -> None:
    dir_for_files = get_dir_name(file_path)
    if not os.path.exists(dir_for_files):
        os.mkdir(dir_for_files)
    response = requests.get(link)
    url = urlparse(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    logger.info(f'Downloading resources to {dir_for_files}')
    with open(file_path, 'r+') as f:
        for key_tag, value_tag in tags.items():
            items = soup.find_all(key_tag)
            bar = ChargingBar(f'Downloading {key_tag}', max=len(items))
            for item in items:
                bar.next()
                item_full_name = get_resource_full_name(link, item, value_tag)
                if not item_full_name:
                    continue
                abs_path = os.path.join(dir_for_files, item_full_name)
                relative_path = os.path.join(get_dir_name(get_name(f'{url.netloc}{url.path}')), item_full_name)
                tag_link = urljoin(link, item[value_tag])
                response_tag = get_response(tag_link)
                try:
                    get_content(abs_path, response_tag.content)
                except OSError as e:
                    logger.error(f"Can't open file {abs_path}")
                    raise KnownError() from e
                item[value_tag] = relative_path
            bar.finish()
        f.write(soup.prettify())
