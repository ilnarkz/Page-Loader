import os.path
import tempfile

from page_loader.save_page import save_page


TEXT = '<!doctype html><html lang="ru"></html>'


def test_save_page():
    with tempfile.TemporaryDirectory() as tmp_dir:
        file_path = os.path.join(tmp_dir, 'index.html')
        save_page(TEXT, file_path)
        with open(file_path, 'r') as f:
            assert f.read() == TEXT
