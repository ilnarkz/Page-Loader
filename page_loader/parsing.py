import os
from typing import List, Tuple, Union, Optional, Any
from urllib.parse import urlparse, urljoin
import bs4.element
from bs4 import BeautifulSoup
from page_loader.create_directory import create_directory
from page_loader.naming import tags, get_dir_name, get_name


def parse_page(content: str, link: str, file_path: str) -> (str, List[Tuple[str, str]]):
    soup = BeautifulSoup(content, 'html.parser')
    items = soup.find_all(tags.keys())
    resources_links = []
    if not items:
        return soup.prettify(), resources_links
    dir_for_files = create_directory(file_path)
    for item in items:
        url = urlparse(link)
        value_tag = tags[item.name]
        item_full_name = get_resource_full_name(link, item)
        if not item_full_name:
            continue
        absolute_path = os.path.join(dir_for_files, item_full_name)
        relative_path = os.path.join(get_dir_name(get_name(f'{url.netloc}{url.path}')), item_full_name)
        tag_link = urljoin(link, item[value_tag])
        resources_links.append((tag_link, absolute_path))
        item[value_tag] = relative_path
    return soup.prettify(), resources_links


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
