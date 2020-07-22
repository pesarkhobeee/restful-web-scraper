#!/usr/bin/env python3

import argparse
import logging
import sys
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from fake_useragent import UserAgent
from lxml import html


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        ua = UserAgent()
        header = {'User-Agent': str(ua.chrome)}
        with closing(get(url, headers=header, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        raise Exception(
                'Error during requests to {0} : {1}'.format(url, str(e)))


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)

def get_movie(args):
    """
    Downloads the movie page from Amazon
    and extract the information
    """
    url = args.base_url + args.MovieID
    response = simple_get(url)

    if response is not None:
        tree = html.fromstring(response)
        title = tree.xpath('//h1[@data-automation-id="title"]/text()')[0]
        date = tree.xpath('//span[@data-automation-id="release-year-badge"]/text()')[0]
        actors = tree.xpath('//a[@class="_1NNx6V"]/text()')
        image = tree.xpath('//img[@id="atf-thumb"]/@src')
        similar_ids = tree.xpath('//li[@class="_2AgxOB"]//a/@href')
        similar_ids = [i.split('/')[4] for i in similar_ids]
        result = {
                "title": title,
                "release_year": date,
                "actors": actors,
                "poster": image,
                "similar_ids": similar_ids}
        return(result)

    # Raise an exception if we failed to get any data from the url
    raise Exception('Error retrieving contents at {}'.format(url))

def main(args):
    try:
        print(get_movie(args))
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
        '--base-url', type=str, default="https://www.amazon.de/gp/product/",
        help='The base URL to join with Movie ID'
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
