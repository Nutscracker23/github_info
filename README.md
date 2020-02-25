Requirements:

    Python >= 3.8
    
Env requirements:

    AUTH_TOKEN - Github Personal access tokens. Details: https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line)
    
Start example:
    
    python main.py --url https://github.com/microsoft/TypeScript
    or
    python main.py --url git://github.com/microsoft/TypeScript.git
    
Arguments:
  * _--url_ - Url to github repo. Requirement
  * _--start_date_ - Analysis start date in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format. If not set analyzes from the first data
  * _--end_date_ - Analysis end date in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format. If not set analyzes up to the current time
  * _--branch_ - Analyzed branch. Default: master

Example with all arguments:
    
    python main.py --url https://github.com/microsoft/TypeScript --start_date 2019-01-01 --end_date 2020-01-01 --branch master