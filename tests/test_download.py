import tempfile
import requests
import requests_mock
from pageloader.download import download

URL = 'https://ru.hexlet.io/courses'
TEXT = "URL's content"


def test_correct_response():
    response = requests.get(URL)
    assert response.ok


def test_download_url():
    with requests_mock.Mocker() as m:
        m.get(URL, text=TEXT)
        with tempfile.TemporaryDirectory() as tempdir:
            path_file = download(URL, tempdir)
            with open(path_file, 'r') as f:
                assert f.read() == TEXT
