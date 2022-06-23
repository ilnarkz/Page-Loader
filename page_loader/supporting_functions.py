import logging
import os
import re
from typing import Union, Optional, Any
from urllib.parse import urlparse, urljoin
import bs4.element
from bs4 import BeautifulSoup

from page_loader.known_error import KnownError

tags = {'link': 'href',
        'img': 'src',
        'script': 'src'}


def get_name(link: str) -> str:
    return re.sub(r'[\W_]', '-', link)


def get_html_file(link: str) -> str:
    link_name, link_extension = os.path.splitext(link)
    if link_extension != '.html':
        link_name += link_extension
    url = urlparse(link)
    return get_name(f'{url.netloc}{url.path}') + '.html'


def get_dir_name(file_path: str) -> str:
    link_name, link_extension = os.path.splitext(file_path)
    return link_name + '_files'


def get_resource_full_name(link: str, item: bs4.element.Tag) -> Union[Optional[str], Any]:
    url = urlparse(link)
    value_tag = tags[item.name]
    if not item.has_attr(value_tag):
        return None
    item_name, item_extension = os.path.splitext(item[value_tag])
    if not item_extension:
        item_extension = '.html'
    if item_name.startswith('http'):
        item_name_parse = urlparse(item_name)
        if item_name_parse.netloc != url.netloc:
            return None
        item_full_name = get_name(f'{item_name_parse.netloc}{item_name_parse.path}') + item_extension
    else:
        item_full_name = get_name(f'{url.netloc}') + get_name(item_name) + item_extension
    return item_full_name


def create_dir(file_path: str):
    dir_for_files = get_dir_name(file_path)
    try:
        os.mkdir(dir_for_files)
    except OSError as err:
        logging.error(f"Can't create directory {dir_for_files}. Directory already exists")
        raise KnownError() from err
    return dir_for_files


def save_page(data: str, file_path: str):
    with open(file_path, 'w') as f:
        f.write(data)


def parse_page(content: bytes, link: str, dir_for_files: str):
    soup = BeautifulSoup(content, 'html.parser')
    items = soup.find_all(tags.keys())
    resources_links = []
    for item in items:
        url = urlparse(link)
        value_tag = tags[item.name]
        item_full_name = get_resource_full_name(link, item)
        if not item_full_name:
            continue
        abs_path = os.path.join(dir_for_files, item_full_name)
        relative_path = os.path.join(get_dir_name(get_name(f'{url.netloc}{url.path}')), item_full_name)
        tag_link = urljoin(link, item[value_tag])
        resources_links.append((tag_link, abs_path))
        item[value_tag] = relative_path
    return soup.prettify(), resources_links
