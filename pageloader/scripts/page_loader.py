import argparse
import os
from pageloader.download import download


def main():
    parser = argparse.ArgumentParser(description='Page Loader')
    parser.add_argument('url_page')
    parser.add_argument('--output',
                        help='get current directory',
                        default=os.getcwd())
    args = parser.parse_args()
    print(download(args.url_page, args.tmp_dir))


if __name__ == '__main__':
    main()
