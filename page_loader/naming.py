import os
import re
from urllib.parse import urlparse

tags = {'link': 'href',
        'img': 'src',
        'script': 'src'}


def get_name(link: str) -> str:
    return re.sub(r'[\W_]', '-', link)


def get_html_file_name(link: str) -> str:
    link_name, link_extension = os.path.splitext(link)
    url = urlparse(link_name)
    if link_extension != '.html':
        url = urlparse(link)
        link_name += link_extension
    return get_name(f'{url.netloc}{url.path}') + '.html'


def get_dir_name(file_path: str) -> str:
    link_name, link_extension = os.path.splitext(file_path)
    return link_name + '_files'
