import os
import re
from urllib.parse import urlparse

import requests


def get_name(link):
    return re.sub(r'[\W_]', '-', link)


def get_response(link):
    return requests.get(link)


def get_html_file(link):
    link_name, link_extension = os.path.splitext(link)
    if link_extension != '.html':
        link_name += link_extension
    url = urlparse(link)
    return get_name(f'{url.netloc}{url.path}') + '.html'


def get_dir_name(file_path):
    link_name, link_extension = os.path.splitext(file_path)
    return link_name + '_files'


def get_resource_full_name(link, item, value_tag):
    url = urlparse(link)
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


def get_content(path, data):
    mode = 'w'
    if isinstance(data, bytes):
        mode = 'wb'
    with open(path, mode) as tag_content:
        tag_content.write(data)
