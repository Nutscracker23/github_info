from connection import MainProcess
from utils import get_arguments


def main() -> None:
    args_dict = get_arguments()
    owner, repo = args_dict.get('url').values()
    branch = args_dict.get('branch')
    start_date = args_dict.get('start_date')
    end_date = args_dict.get('end_date')

    print('Owner: ', owner)
    print('Repo: ', repo)
    print('Branch: ', branch)
    print('Start date: ', start_date or 'All')
    print('End date: ', end_date or 'All')
    print('\r')

    process = MainProcess(owner, repo, branch, start_date, end_date)
    process.run()
    process.print_result()


if __name__ == '__main__':
    main()
