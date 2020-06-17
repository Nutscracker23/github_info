from datetime import datetime, timedelta

TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


class BaseStore(object):
    def __init__(self, start_date, end_date):
        self.count = 0
        self.data = {}
        self.check_date = datetime.now() - timedelta(days=30)
        self.start_date = start_date
        self.end_date = end_date

    def __str__(self):
        return '{}: {}'.format(self.__class__.__name__, self.count)

    def add_data(self, added_data: list):
        pass

    def print_data(self):
        return self.__str__()

    def parse_data(self):
        return self.data


class CommitsStore(BaseStore):
    def add_data(self, added_data: list):
        for commit in added_data:
            author = commit.get('author')
            if author:
                author_username = author.get('login')
                if author_username not in self.data:
                    self.data[author_username] = 1
                else:
                    self.data[author_username] += 1
            self.count += 1

    def print_data(self):
        authors = sorted(self.data.items(), key=lambda x: x[1], reverse=True)
        print("Commits stats".center(30, '-'))
        print("#  ", "Count:", "Username:")
        for i, author in enumerate(list(authors[:30]), 1):
            print(str(i).ljust(3), str(author[1]).ljust(6), author[0])
        print("Total count:", self.count)
        print('\r')


class PullsStore(BaseStore):
    def __init__(self, start_date, end_date):
        super(PullsStore, self).__init__(start_date, end_date)
        self.data = {
            'open': 0,
            'closed': 0,
            'forgotten': 0,
        }
        self.check_date = datetime.now() - timedelta(days=30)

    def add_data(self, added_data: list):
        for pull in added_data:
            created_at = datetime.strptime(pull.get('created_at'), TIME_FORMAT)
            if (self.start_date and created_at < self.start_date) or (self.end_date and created_at > self.end_date):
                continue

            state = pull.get('state')
            self.data[state] += 1
            if state == 'open' and created_at < self.check_date:
                self.data['forgotten'] += 1
            self.count += 1

    def print_data(self):
        print("Pull Requests stats".center(30, '-'))
        print("Status:".ljust(15), "Count:")
        for pull in self.data.items():
            print(pull[0].ljust(15), pull[1])
        print("Total count: ", self.count)
        print('\r')


class IssuesStore(BaseStore):
    def __init__(self, start_date, end_date):
        super(IssuesStore, self).__init__(start_date, end_date)
        self.data = {
            'open': 0,
            'closed': 0,
            'forgotten': 0,
        }
        self.check_date = datetime.now() - timedelta(days=14)

    def add_data(self, added_data: list):
        for issue in added_data:
            if issue.get('pull_request'):
                continue

            created_at = datetime.strptime(issue.get('created_at'), TIME_FORMAT)
            if (self.start_date and created_at < self.start_date) or (self.end_date and created_at > self.end_date):
                continue

            state = issue.get('state')
            self.data[state] += 1
            if state == 'open' and created_at < self.check_date:
                self.data['forgotten'] += 1
            self.count += 1

    def print_data(self):
        issues = self.parse_data()
        print("Issues stats".center(30, '-'))
        print("Status:".ljust(15), "Count:")
        for issue in issues.items():
            print(issue[0].ljust(15), issue[1])
        print("Total count: ", self.count)
        print('\r')
