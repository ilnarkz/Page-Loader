import argparse
import os
from pageloader.download import download_url


def main():
    parser = argparse.ArgumentParser(description='Page Loader')
    parser.add_argument('url_page')
    parser.add_argument('--output',
                        help='get current directory',
                        default=os.getcwd())
    args = parser.parse_args()
    print(download_url(args.url_page, args.output))


if __name__ == '__main__':
    main()
