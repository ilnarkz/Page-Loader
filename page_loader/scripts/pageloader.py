import argparse
import os
import sys
from page_loader.download import download
from page_loader.known_error import KnownError


def main():
    parser = argparse.ArgumentParser(description='Page Loader')
    parser.add_argument('url_page')
    parser.add_argument('--output',
                        help='get current directory',
                        default=os.getcwd())
    args = parser.parse_args()
    try:
        download(args.url_page, args.output)
    except KnownError():
        sys.exit(1)


if __name__ == '__main__':
    main()
