import logging
import os
from urllib.parse import urlparse, urljoin
import requests
from pageloader.known_error import KnownError
from bs4 import BeautifulSoup
from pageloader.get_correct_name import get_name, get_response, get_dir_name, get_content, get_html_file, \
    get_resource_full_name


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


tags = {'link': 'href',
        'img': 'src',
        'script': 'src'}


def download_url(link, path=os.getcwd()):
    logger.info(f'Requested url {link}')
    logger.info(f'Output path {path}')
    try:
        os.makedirs(path, exist_ok=True)
    except PermissionError as e:
        logger.error(f"Can't create directory {path}. Invalid path")
        raise KnownError() from e
    downloaded_url_name = get_html_file(link)
    file_path = os.path.join(path, downloaded_url_name)
    response = get_response(link)
    try:
        with open(file_path, 'wb') as f:
            f.write(response.content)
    except ConnectionError as error1:
        logger.error(f"Download failed: status code {response.status_code}")
        raise KnownError() from error1
    except OSError as error2:
        logger.error(f"Can't open file {file_path}")
        raise KnownError() from error2
    download_data(link, file_path)
    logger.info(f'Webpage was downloaded as {file_path}')
    return file_path


def download_data(link, file_path):
    dir_for_files = get_dir_name(file_path)
    if not os.path.exists(dir_for_files):
        os.mkdir(dir_for_files)
    response = requests.get(link)
    url = urlparse(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    with open(file_path, 'r+') as f:
        for key_tag, value_tag in tags.items():
            items = soup.find_all(key_tag)
            for item in items:
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
                    raise KnownError from e
                item[value_tag] = relative_path
        f.write(soup.prettify())
