import os
import re
import requests


def download(url, path=os.getcwd()):
    os.makedirs(path, exist_ok=True)
    filename, file_extension = os.path.splitext(url)
    filename_without_scheme = filename.split('//')[1]
    downloaded_file_name = re.sub('[\\W_]', '-', filename_without_scheme)
    file_path = os.path.join(path, downloaded_file_name) + '.html'
    response = requests.get(url, stream=True)
    if response.ok:
        with open(file_path, 'wb') as f:
            f.write(response.content)
        return file_path
    else:
        print(f"Download failed: status code {response.status_code}")
