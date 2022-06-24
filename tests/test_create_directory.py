import os
import tempfile
from page_loader.create_directory import create_directory


def test_create_directory():
    with tempfile.TemporaryDirectory() as tmp_dir:
        dir_for_files = create_directory(tmp_dir)
        assert os.path.exists(dir_for_files)
