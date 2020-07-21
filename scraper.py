#!/usr/bin/env python3

import argparse
import logging
import sys
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
# from bs4 import BeautifulSoup


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        logging.critical(
                'Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)

def main(args):
    try:
        print(args.MovieID)
        raw_html = simple_get('http://pathseeker.ir')
        print(len(raw_html))
    except Exception as e:
        logging.critical("Fatal error hapend: {}".format(e))
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MovieID")
    parser.add_argument(
        'MovieID', type=str,
        help='ID of the movie in Amazon store'
    )
    parser.add_argument(
        '--log-level', type=str, default="WARNING",
        help='Set the logging level. Defaults to WARNING.'
    )
    parsed_args = parser.parse_args()
    logging.getLogger()
    logging.basicConfig(
        format='%(asctime)s %(levelname)s %(message)s',
        level=parsed_args.log_level,
        datefmt='%Y-%m-%dT%H:%M:%S%z')
    logging.info(
        "Starting with given arguments: {}".format(parsed_args)
    )
    main(parsed_args)
