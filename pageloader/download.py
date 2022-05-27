import os
from urllib.parse import urlparse, urljoin

import requests
from bs4 import BeautifulSoup

from pageloader.get_correct_name import get_name, get_response, get_dir_name, get_content, get_html_file, \
    get_resource_full_name

tags = {'link': 'href',
        'img': 'src',
        'script': 'src'}


def download_url(link, path=os.getcwd()):
    os.makedirs(path, exist_ok=True)
    downloaded_url_name = get_html_file(link)
    file_path = os.path.join(path, downloaded_url_name)
    response = get_response(link)
    if response.ok:
        with open(file_path, 'wb') as f:
            f.write(response.content)
    else:
        raise Exception(f"Download failed: status code {response.status_code}")
    download_data(link, file_path)
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
                get_content(abs_path, response_tag.content)
                item[value_tag] = relative_path
        f.write(soup.prettify())
