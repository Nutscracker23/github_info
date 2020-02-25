import json
from http.client import HTTPResponse
from multiprocessing.dummy import Pool

from connection import Connection
from github import CommitsStore, PullsStore, IssuesStore
from utils import parse_link


class MainProcess(object):
    def __init__(self, owner: str, repo: str, branch: str, start_date: str, end_date: str):
        self.owner = owner
        self.repo = repo
        self.branch = branch
        self.start_date = start_date
        self.end_date = end_date

        self.connection = Connection()
        self.commits_store = CommitsStore(start_date, end_date)
        self.pulls_store = PullsStore(start_date, end_date)
        self.issues_store = IssuesStore(start_date, end_date)

    def run(self):
        self.get_commits()
        self.get_issues()
        self.get_pulls()

    def print_result(self):
        self.commits_store.print_data()
        self.issues_store.print_data()
        self.pulls_store.print_data()

    def get_data(self, store: str, path: str = '', **kwargs) -> HTTPResponse:
        response = self.connection.get_response(path, **kwargs)
        getattr(self, store).add_data(json.loads(response.read()))
        return response

    def get_data_pool(self, request_data: dict, parsed_link_last: dict):
        last_page = int(parsed_link_last.get('page', 2))
        request_data['path'] = parsed_link_last.get('path')
        map_args = [{'page': page, **request_data} for page in range(2, last_page + 1)]
        pool = Pool()
        pool.map(self.get_data_start, map_args)
        pool.close()
        pool.join()

    def get_data_start(self, args: dict):
        return self.get_data(**args)

    def get_commits(self):
        request_path = '/repos/{owner}/{repo}/commits'.format(
            owner=self.owner,
            repo=self.repo
        )
        request_data = {
            'store': 'commits_store',
            'path': request_path,
            'sha': self.branch,
        }
        if self.start_date:
            request_data['since'] = self.start_date
        if self.end_date:
            request_data['until'] = self.end_date
        response = self.get_data(**request_data)

        link_header = response.getheader('Link')
        parsed_link = parse_link(link_header)
        parsed_link_last = parsed_link.get('last')
        if parsed_link and parsed_link_last:
            self.get_data_pool(request_data, parsed_link_last)

    def get_data_by_state(self, request_data: dict, state: str):
        request_data['state'] = state
        response = self.get_data(**request_data)
        link_header = response.getheader('Link')
        parsed_link = parse_link(link_header)
        parsed_link_last = parsed_link.get('last')

        if parsed_link and parsed_link_last:
            self.get_data_pool(request_data, parsed_link_last)

    def get_issues(self):
        request_path = '/repos/{owner}/{repo}/issues'.format(
            owner=self.owner,
            repo=self.repo
        )
        request_data = {
            'store': 'issues_store',
            'path': request_path,
        }
        self.get_data_by_state(request_data, 'all')

    def get_pulls(self):
        request_path = '/repos/{owner}/{repo}/pulls'.format(
            owner=self.owner,
            repo=self.repo
        )
        request_data = {
            'store': 'pulls_store',
            'path': request_path,
            'head': self.branch,
        }
        self.get_data_by_state(request_data, 'all')