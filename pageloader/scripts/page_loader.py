import argparse
import os
import sys
from pageloader.download import download_url
from pageloader.known_error import KnownError


def main():
    parser = argparse.ArgumentParser(description='Page Loader')
    parser.add_argument('url_page')
    parser.add_argument('--output',
                        help='get current directory',
                        default=os.getcwd())
    args = parser.parse_args()
    try:
        print(download_url(args.url_page, args.output))
    except KnownError:
        sys.exit(1)


if __name__ == '__main__':
    main()
