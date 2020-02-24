import argparse
import re
import time
from datetime import datetime
from http.client import HTTPResponse
from urllib.parse import urlparse, parse_qs

REL_ALIASES = {
    'rel="first"': 'first',
    'rel="prev"': 'prev',
    'rel="next"': 'next',
    'rel="last"': 'last',
}


def get_arguments() -> dict:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", type=url_type)
    parser.add_argument("--start_date", type=datetime_type, default='', help='Timestamp in ISO 8601')
    parser.add_argument("--end_date", type=datetime_type, default='', help='Timestamp in ISO 8601')
    parser.add_argument("--branch", type=str, default='master')
    args = parser.parse_args()
    args_dict = vars(args)
    return args_dict


def url_type(string: str) -> dict:
    if not string:
        raise argparse.ArgumentTypeError("Set url")
    regex = r"github.com/(?P<owner>[\d\w]+)/(?P<repo>[\d\w]+)[/]?$"
    pattern = re.compile(regex)
    search_result = pattern.search(string)

    try:
        result = {
            'owner': search_result.group('owner'),
            'repo': search_result.group('repo')
        }
    except AttributeError:
        raise argparse.ArgumentTypeError("Set correct url")

    return result


def datetime_type(string: str):
    result = ''
    if string:
        try:
            result = datetime.fromisoformat(string)
        except ValueError:
            raise argparse.ArgumentTypeError("Set correct date")
    return result


def check_rate_limit(response: HTTPResponse):
    remaining_header = response.getheader('X-RateLimit-Remaining')
    print(remaining_header)

    if not remaining_header:
        reset_header = response.getheader('X-RateLimit-Reset')
        now = time.time()
        time.sleep(int(reset_header) - now + 1)


def parse_link(header: str) -> dict:
    result = {}
    if header:
        links = header.split(', ')
        for link_str in links:
            link, rel = link_str.split('; ')
            parsed_link = urlparse(link.replace('<', '').replace('>', ''))
            query_dict = parse_qs(parsed_link.query)

            result[REL_ALIASES[rel]] = {
                'path': parsed_link.path,
                'page': query_dict.get('page').pop(),
            }

    return result
