import logging
import os
import tempfile
import pytest
import requests_mock
from pageloader.known_error import KnownError

from pageloader.download import download_url


URL = 'https://ru.hexlet.io/courses'
CSS_URL = 'https://ru.hexlet.io/assets/application.css'
JS_URL = 'https://ru.hexlet.io/packs/js/runtime.js'
PNG_URL = 'https://ru.hexlet.io/assets/professions/nodejs.png'
DOWNLOADED_PAGE = 'tests/fixture/downloaded_html.html'
INNER_LINK = 'tests/fixture/downloaded_html_files/inner_link.html'
PAGE = 'tests/fixture/downloaded_html_files/before_download_data.html'
CSS = 'tests/fixture/downloaded_html_files/css_file.css'
JS = 'tests/fixture/downloaded_html_files/js_file.js'
PNG = 'tests/fixture/downloaded_html_files/nodejs.png'
INNER_HTML_ASSETS = 'ru-hexlet-io-courses_files/ru-hexlet-io-courses.html'
JS_ASSETS = 'ru-hexlet-io-courses_files/ru-hexlet-io-packs-js-runtime.js'
CSS_ASSETS = 'ru-hexlet-io-courses_files/ru-hexlet-io-assets-application.css'
PNG_ASSETS = 'ru-hexlet-io-courses_files/ru-hexlet-io-assets-professions-nodejs.png'
URL_FIXTURE = 'ru-hexlet-io-courses.html'


def read_file(file_path, mode='r'):
    with open(file_path, mode) as f:
        return f.read()


@pytest.mark.parametrize('received, expected', [(URL_FIXTURE, DOWNLOADED_PAGE),
                                                (JS_ASSETS, JS),
                                                (CSS_ASSETS, CSS),
                                                (INNER_HTML_ASSETS, INNER_LINK)])
def test_save_file(received, expected):
    with requests_mock.Mocker() as m:
        m.get(URL, text=read_file(PAGE))
        m.get(URL, text=read_file(INNER_LINK))
        m.get(PNG_URL, content=read_file(PNG, 'rb'))
        m.get(CSS_URL, text=read_file(CSS))
        m.get(JS_URL, text=read_file(JS))
        with tempfile.TemporaryDirectory() as temp_dir:
            download_url(URL, temp_dir)
            received_file = os.path.join(temp_dir, received)
            received_png = os.path.join(temp_dir, PNG_ASSETS)
            assert read_file(received_file) == read_file(expected)
            assert read_file(received_png, 'rb') == read_file(PNG, 'rb')


def test_errors():
    with requests_mock.Mocker() as m:
        m.get(URL, exc=KnownError)
        with tempfile.TemporaryDirectory() as temp_dir:
            with pytest.raises(KnownError):
                download_url(URL, temp_dir)
